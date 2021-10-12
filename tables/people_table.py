from dbtable import *


class PeopleTable(DbTable):
    def table_name(self):
        return self.dbconn.prefix + "people"

    def columns(self):
        return {"id": ["SERIAL", "PRIMARY KEY"],
                "last_name": ["varchar(32)", "NOT NULL"],
                "first_name": ["varchar(32)", "NOT NULL"],
                "second_name": ["varchar(32)"]}

    def find_by_id(self, num):
        sql = f"SELECT * FROM {self.table_name() } WHERE id = %s"
        cur = self.dbconn.conn.cursor()
        cur.execute(sql, [num])
        return cur.fetchone()

    def find_by_last_name(self, last_name):
        sql = f"SELECT * FROM {self.table_name() } WHERE last_name like %s"
        cur = self.dbconn.conn.cursor()
        last_name = last_name[:] + '%'
        cur.execute(sql, [last_name])
        return cur.fetchall()
