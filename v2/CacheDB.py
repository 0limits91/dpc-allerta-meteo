import sqlite3

class CacheDB:
    def __init__(self, db):
        self.db = sqlite3.connect(db)
        self.db.execute('''CREATE TABLE IF NOT EXISTS cache
                       (zona text, data text, file_name text )''')
    #https://stackoverflow.com/questions/198692/can-i-pickle-a-python-dictionary-into-a-sqlite3-text-field

    def getInstance(self):
        return self.db.cursor()

    def insert(self,data, alert):
        db = self.getInstance()
        db.execute("insert into cache (zona, data, file_name) values ('"+alert.nome_zona+"','"+str(data)+"','"+alert.nome_file+"')")
        self.db.commit()

    def get(self, sql):
        #try:
            db = self.getInstance()
            db.execute(str(sql))
            rows = db.fetchall()
        #except:
        #    return []
        #else:
            return rows

    def execute(self, sql):
        db = self.getInstance()
        db.execute(str(sql))
        self.db.commit()

    def close(self):
        db = self.getInstance()
        self.db.close()