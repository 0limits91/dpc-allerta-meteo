class BollettinoMeteo:
    def __init__(self):
        __city = None

        __nome_zona = None
        __info_zona = None

        __allerta_criticita = None
        __info_criticita = None

        __allerta_idrogeologico = None
        __info_idrogeologico = None

        __allerta_temporali = None
        __info_temporali = None

        __allerta_idraulico = None
        __info_idraulico = None

        __città_interessate = None
        __geometry = None
        __nome_file = None

        __isValid = False

    @property
    def isValid(self):
        return self.__isValid

    @isValid.setter
    def isValid(self, valid):
        self.__isValid = valid

    @property
    def città(self):
        return self.__city

    @città.setter
    def città(self, city):
        self.__city = city

    #Zona
    @property
    def info_zona(self):
        return self.__info_zona

    @info_zona.setter
    def info_zona(self, info):
        self.__info_zona = info

    @property
    def nome_zona(self):
        return self.__nome_zona

    @nome_zona.setter
    def nome_zona(self, nome):
        self.__nome_zona = nome

    #Criticità
    @property
    def allerta_criticità(self):
        return self.__allerta_criticità

    @allerta_criticità.setter
    def allerta_criticità(self, allerta):
        self.__allerta_criticità = allerta

    @property
    def info_criticità(self):
        return self.__info_criticità

    @info_criticità.setter
    def info_criticità(self, info):
        self.__info_criticità = info

    #Idrogeologico
    @property
    def allerta_idrogeologico(self):
        return self.__allerta_idrogeologico

    @allerta_idrogeologico.setter
    def allerta_idrogeologico(self, allerta):
        self.__allerta_idrogeologico = allerta

    @property
    def info_idrogeologico(self):
        return self.__info_idrogeologico

    @info_idrogeologico.setter
    def info_idrogeologico(self, info):
        self.__info_idrogeologico = info

    #Temporali
    @property
    def allerta_temporali(self):
        return self.__allerta_temporali

    @allerta_temporali.setter
    def allerta_temporali(self, allerta):
        self.__allerta_temporali = allerta

    @property
    def info_temporali(self):
        return self.__info_temporali

    @info_temporali.setter
    def info_temporali(self, info):
        self.__info_temporali = info

    #Idraulico
    @property
    def allerta_idraulico(self):
        return self.__allerta_idraulico

    @allerta_idraulico.setter
    def allerta_idraulico(self, allerta):
        self.__allerta_idraulico = allerta

    @property
    def info_idraulico(self):
        return self.__info_criticità

    @info_idraulico.setter
    def info_idraulico(self, info):
        self.__info_idraulico = info

    #Geometry
    @property
    def geometry(self):
        return self.__geometry

    @geometry.setter
    def geometry(self, geometry):
        self.__geometry = geometry

    #Comuni
    @property
    def città_interessate(self):
        return self.__città_interessate

    @città_interessate.setter
    def città_interessate(self, città):
        self.__città_interessate = città

    # Nome File
    @property
    def nome_file(self):
        return self.__nome_file

    @nome_file.setter
    def nome_file(self, nome_file):
        self.__nome_file = nome_file