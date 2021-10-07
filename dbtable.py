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

    def create(self):
        sql = "CREATE TABLE " + self.table_name() + "("
        arr = [k + " " + " ".join(v) for k, v in self.columns().items()]
        sql += ", ".join(arr + self.table_constraints())
        sql += ")"
        cur = self.dbconn.conn.cursor()
        cur.execute(sql)
        self.dbconn.conn.commit()
        return

    def drop(self):
        sql = "DROP TABLE IF EXISTS " + self.table_name()
        cur = self.dbconn.conn.cursor()
        cur.execute(sql)
        self.dbconn.conn.commit()
        return

    def insert_one(self, vals):
        sql = f"""INSERT INTO {self.table_name()} ({", ".join(self.column_names_without_id())}) VALUES({", ".join(["%s" for _ in range(len(vals))]) } )"""
        cur = self.dbconn.conn.cursor()
        cur.execute(sql, (*vals, ))
        self.dbconn.conn.commit()
        return

    def first(self):
        sql = "SELECT * FROM " + self.table_name()
        sql += " ORDER BY "
        sql += ", ".join(self.primary_key())
        cur = self.dbconn.conn.cursor()
        cur.execute(sql)
        return cur.fetchone()

    def last(self):
        sql = "SELECT * FROM " + self.table_name()
        sql += " ORDER BY "
        sql += ", ".join([x + " DESC" for x in self.primary_key()])
        cur = self.dbconn.conn.cursor()
        cur.execute(sql)
        return cur.fetchone()

    def all(self):
        sql = "SELECT * FROM " + self.table_name()
        sql += " ORDER BY "
        sql += ", ".join(self.primary_key())
        cur = self.dbconn.conn.cursor()
        cur.execute(sql)
        return cur.fetchall()

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
        return rows and len(rows) > 0

    def delete_one_by_field(self, field, field_val):
        is_exist = self.check_field_exist(field, str(field_val))
        if (is_exist):
            self.dbconn.conn.cursor().execute(
                sql.SQL(
                    f"""DELETE FROM {self.table_name()}
                        WHERE {{}} = %s"""
                ).format(sql.Identifier(field)), (field_val,))

        return is_exist
