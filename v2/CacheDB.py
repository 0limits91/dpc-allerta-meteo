import sqlite3
from BollettinoMeteo import BollettinoMeteo
class CacheDB:
    def __init__(self, db):
        self.db = sqlite3.connect(db)
        self.__allerta = BollettinoMeteo()
        self.__cache = []
        self.db.execute('''CREATE TABLE IF NOT EXISTS cache
                               (data text,city text, nome_zona text, info_zona text, 
                               allerta_criticita text, info_criticita text,  
                               allerta_idrogeologico text, info_idrogeologico text,
                               allerta_temporali text, info_temporali text,  
                               allerta_idraulico text, info_idraulico text,
                               città_interessate text, geometry text, nome_file text 
                               )''')

    def getInstance(self):
        return self.db.cursor()

    def insertReport(self,data, alert):
        db = self.getInstance()
        db.execute("insert into cache ("
                   +"data,city,"
                   +"nome_zona, info_zona,"
                   +"allerta_criticita,info_criticita,"
                   +"allerta_idrogeologico, info_idrogeologico,"
                   +"allerta_temporali,info_temporali,"
                   +"allerta_idraulico,info_idraulico,"
                   +"città_interessate, geometry, nome_file) "
                   +"values ('"+str(data)+"', '"+alert.city+"', '"+alert.nome_zona+"', '"+alert.info_zona+"', "
                   +"'"+alert.allerta_criticità+"','"+alert.info_criticità+"',"
                   +"'"+alert.allerta_idrogeologico+"','"+alert.info_idrogeologico+"',"
                   +"'"+alert.allerta_temporali+"','"+alert.info_temporali+"',"
                   +"'"+alert.allerta_idraulico+"','"+alert.info_idraulico+"',"
                   +"'Città Interesate','Geometrie','"+alert.nome_file+"')")
        self.db.commit()

    def getReport(self, sql):
        db = self.getInstance()
        db.execute(str(sql))
        rows = db.fetchall()

        for row in rows:
            columns = ["data", "city", "nome_zona", "info_zona",
                       "allerta_criticita", "info_criticita", "allerta_idrogeologico",
                       "info_idrogeologico", "allerta_temporali", "info_temporali",
                       "allerta_idraulico", "info_idraulico", "città_interessate",
                       "geometry", "nome_file"]
            self.__cache = dict(zip(columns, row))

            self.__allerta.city = self.__cache["city"]

            self.__allerta.info_zona = self.__cache["nome_zona"]
            self.__allerta.nome_zona = self.__cache["info_zona"]
            self.__allerta.geometry = ""

            self.__allerta.info_criticità = self.__cache["info_criticita"]
            self.__allerta.allerta_criticità = self.__cache["allerta_criticita"]

            self.__allerta.info_idrogeologico = self.__cache["info_idrogeologico"]
            self.__allerta.allerta_idrogeologico = self.__cache["allerta_idrogeologico"]

            self.__allerta.info_idraulico = self.__cache["info_idraulico"]
            self.__allerta.allerta_idraulico = self.__cache["allerta_idraulico"]

            self.__allerta.info_temporali = self.__cache["info_temporali"]
            self.__allerta.allerta_temporali = self.__cache["allerta_temporali"]

            self.__allerta.città_interessate = ""
            self.__allerta.nome_file = self.__cache["nome_file"]

        return self.__cache

    def getAlert(self):
        return self.__allerta

    def execute(self, sql):
        db = self.getInstance()
        db.execute(str(sql))
        self.db.commit()

    def close(self):
        self.db.close()