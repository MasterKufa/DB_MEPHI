from dbtable import *


class AutoTable(DbTable):
    def table_name(self):
        return self.dbconn.prefix + "autos"

    def columns(self):
        return {"brand": ["varchar(12)", "NOT NULL"],
                "model": ["varchar(12)", "NOT NULL"],
                "color": ["varchar(12)", "NOT NULL"],
                "identity": ["varchar(12)", "PRIMARY KEY"],
                }
