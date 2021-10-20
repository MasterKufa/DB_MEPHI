from dbtable import *


class AutoTable(DbTable):
    def table_name(self):
        return self.dbconn.prefix + "autos"

    def columns(self):
        return {"person_id": ["integer", f"REFERENCES {self.dbconn.prefix}people(id) ON DELETE CASCADE"],
                "brand": ["varchar(12)", "NOT NULL"],
                "model": ["varchar(12)", "NOT NULL"],
                "color": ["varchar(12)", "NOT NULL"],
                "identity": ["varchar(12)", "PRIMARY KEY"],
                }

    def all_by_person_id(self, pid):
        sql = f"SELECT * FROM {self.table_name()} WHERE person_id = %s ORDER BY {', '.join(self.primary_key())}"
        cur = self.dbconn.conn.cursor()
        cur.execute(sql, [pid])
        return cur.fetchall()

    def primary_key(self):
        return ['identity']
