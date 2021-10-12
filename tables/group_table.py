from dbtable import *


class GroupTable(DbTable):
    def table_name(self):
        return self.dbconn.prefix + "groups"

    def columns(self):
        return {"person_id": ["integer", f"REFERENCES {self.dbconn.prefix}people(id) ON DELETE CASCADE"],
                "class": ["varchar(12)", "NOT NULL"],
                "speciality": ["varchar(32)", "NOT NULL"],
                "kaf": ["varchar(32)", "NOT NULL"]
                }

    def primary_key(self):
        return ['person_id', 'class']

    def table_constraints(self):
        return ["PRIMARY KEY(person_id, class)"]

    def all_by_person_id(self, pid):
        sql = f"SELECT * FROM {self.table_name()} WHERE person_id = %s ORDER BY {', '.join(self.primary_key())}"
        cur = self.dbconn.conn.cursor()
        cur.execute(sql, [pid])
        return cur.fetchall()
