from dbconnection import *


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
        for i in range(0, len(vals)):
            if type(vals[i]) == str:
                vals[i] = "'" + vals[i] + "'"
            else:
                vals[i] = str(vals[i])
        sql = "INSERT INTO " + self.table_name() + "("
        sql += ", ".join(self.column_names_without_id()) + ") VALUES("
        sql += ", ".join(vals) + ")"
        cur = self.dbconn.conn.cursor()
        cur.execute(sql)
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
        if (isinstance(field, list) and isinstance(field_val, list)):
            cur.execute(
                f"""SELECT * FROM {self.table_name()} WHERE {' AND '.join([f"{x}='{field_val[inx]}'" for  (inx, x) in enumerate(field)])}""")
        else:
            cur.execute(
                f"SELECT * FROM {self.table_name()} WHERE {field}='{field_val}'")
        rows = cur.fetchall()
        return rows and len(rows) > 0

    def delete_one_by_field(self, field, field_val):
        is_exist = self.check_field_exist(field, str(field_val))
        if (is_exist):
            self.dbconn.conn.cursor().execute(
                f"DELETE FROM {self.table_name()} WHERE {field} = '{str(field_val)}'")
        return is_exist
