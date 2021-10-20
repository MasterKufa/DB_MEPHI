from dbconnection import *
from psycopg2 import sql


class DbTable:
    dbconn = None

    def __init__(self):
        return

    def table_name(self):
        return self.dbconn.prefix + "table"

    def columns(self):
        return {"test": ["integer", "PRIMARY KEY"]}

    def column_names(self):
        return self.columns().keys()

    def primary_key(self):
        return ['id']

    def column_names_without_id(self):
        lst = list((self.columns().keys() - ['id']))
        lst.sort()
        return lst

    def table_constraints(self):
        return []

    def run_cursor(self, sql):
        cur = self.dbconn.conn.cursor()
        cur.execute(sql)
        return cur

    def fetch_cursor(self, sql, isSingleFetch):
        cur = self.run_cursor(sql)
        return (cur.fetchone if isSingleFetch else cur.fetchall)()

    def run_cur_with_commit(self, sql):
        self.run_cursor(sql)
        self.dbconn.conn.commit()

    def create(self):
        arr = [k + " " + " ".join(v) for k, v in self.columns().items()]
        sql = f"CREATE TABLE {self.table_name()} ({', '.join(arr + self.table_constraints())})"
        self.run_cur_with_commit(sql)

    def drop(self):
        sql = "DROP TABLE IF EXISTS " + self.table_name()
        self.run_cur_with_commit(sql)

    def insert_one(self, vals):
        sql = f"""INSERT INTO {self.table_name()} ({", ".join(self.column_names_without_id())}) VALUES({", ".join(["%s" for _ in range(len(vals))]) } )"""
        cur = self.dbconn.conn.cursor()
        cur.execute(sql, (*vals, ))
        self.dbconn.conn.commit()

    def first(self):
        sql = f"SELECT * FROM {self.table_name()} ORDER BY {', '.join(self.primary_key())}"
        return self.fetch_cursor(sql, True)

    def last(self):
        sql = f"SELECT * FROM {self.table_name()} ORDER BY {', '.join([x + ' DESC' for x in self.primary_key()])}"
        return self.fetch_cursor(sql, True)

    def all(self):
        sql = f"SELECT * FROM  {self.table_name()} ORDER BY {', '.join(self.primary_key())}"
        return self.fetch_cursor(sql, False)

    def paginate(self, page, per_page):
        sql = f"SELECT * FROM  {self.table_name()} ORDER BY {', '.join(self.primary_key())} OFFSET {(int(page) - 1) * per_page} ROWS LIMIT {per_page}"
        return self.fetch_cursor(sql, False)

    def check_field_exist(self, field, field_val):
        cur = self.dbconn.conn.cursor()
        isList = isinstance(field, list) and isinstance(field_val, list)
        fields = field if isList else [field]
        vals = field_val if isList else [field_val]

        cur.execute(
            sql.SQL(
                f"""SELECT * FROM {self.table_name()}
                    WHERE {" AND ".join(['{} = %s' for _ in range(len(fields))])}"""
            ).format(*[sql.Identifier(x) for x in fields]), (*vals, ))

        rows = cur.fetchall()
        return bool(rows and len(rows) > 0)

    def delete_one_by_field(self, field, field_val):
        is_exist = self.check_field_exist(field, str(field_val))
        if (is_exist):
            self.dbconn.conn.cursor().execute(
                sql.SQL(
                    f"""DELETE FROM {self.table_name()}
                        WHERE {{}} = %s"""
                ).format(sql.Identifier(field)), (field_val,))

        return is_exist
