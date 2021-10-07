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
        cur.execute(sql, (str(num)))
        return cur.fetchone()
