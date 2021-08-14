import io
import json
import requests
import geopandas as gpd
from fiona.io import ZipMemoryFile
from datetime import timedelta, datetime
from BollettinoMeteo import BollettinoMeteo
from tools import formatDateToFilename

class DpcBollettiniRepositoryParser:

    def __init__(self, date):
        self.__URL = "https://api.github.com/repos/pcm-dpc/DPC-Bollettini-Criticita-Idrogeologica-Idraulica/contents/files/all"
        self.__RAW_URL = "https://raw.githubusercontent.com/pcm-dpc/DPC-Bollettini-Criticita-Idrogeologica-Idraulica/master/files/all"
        self.__choice = "oggi"
        self.__city = "Roma"
        self.__jData = json.loads(requests.get(self.__URL).text)
        self.__today = datetime.fromisoformat(str(date))
        self.__yesterday = self.__today - timedelta(days=1)
        self.__zipFileName = ''
        self.__fileName = ''
        self.__allerta = BollettinoMeteo()
        self.__today = formatDateToFilename(self.__today)
        self.__yesterday = formatDateToFilename(self.__yesterday)

    @property
    def choise(self):
        return self.__choise

    @choise.setter
    def choise(self, choise):
        self.__choise = choise

    @property
    def day(self):
        return self.__oggi

    @day.setter
    def day(self, day):
        self.__oggi = day

    @property
    def city(self):
        return self.__city

    @city.setter
    def city(self, city):
        self.__city = city

    def getRemoteZipFileName(self, day_selected):
        #remoteFileNames = []

        for fileInfo in reversed(self.__jData):
            if fileInfo['name'].startswith(day_selected):
                return fileInfo['name']
                break

        #if len(remoteFileNames) == 0:
        return[]

        #return remoteFileNames[-1]

    def parse(self):
        if self.__choise == "ieri":
            day_selected = self.__yesterday
        else:
            day_selected = self.__today

        self.__zipFileName = self.getRemoteZipFileName(day_selected)

        if len(self.__zipFileName) == 0:
            print("Dati giornalieri non ancora inseriti mostro quelli di ieri/oggi")
            day_selected = self.__yesterday
            self.__zipFileName = self.getRemoteZipFileName(day_selected)
            self.choise = "domani"

        if len(self.__zipFileName) == 0:
            print("Data non valida!")
            exit(1)

        self.__fileName = self.__zipFileName.split('_all.zip')[0].split('/')[-1:][0]

        # inizializzazione nomi file zip
        link_zip = self.__RAW_URL + '/' + self.__zipFileName

        # lettura zip in memoria
        data_zip = requests.get(link_zip).content
        zipshp = io.BytesIO(data_zip)
        with (ZipMemoryFile(zipshp)) as memfile:
            day_partial_file = "_today"
            if self.__choise == "domani":
                day_partial_file = "_tomorrow"

            complete_filename = self.__fileName + day_partial_file + ".shp"

            with memfile.open(complete_filename) as src:
                #crs = src.crs
                #gdf = gpd.GeoDataFrame.from_features(src, crs=crs)
                gdf = gpd.GeoDataFrame.from_features(src)

        with open('zone2comuni.json') as json_file:
            data = json.load(json_file)
            for zona, città in data.items():
                for comune in città:
                    if comune == self.__city:
                        item = gdf.loc[gdf['Zona_all'] == zona]
                        self.__allerta.city = self.__city

                        self.__allerta.info_zona = item.iloc[0]["Nome_zona"]
                        self.__allerta.nome_zona = item.iloc[0]["Zona_all"]
                        self.__allerta.geometry  = item.iloc[0]["geometry"]

                        self.__allerta.info_criticità = item.iloc[0]["Criticita"].split('/')[0]
                        self.__allerta.allerta_criticità= item.iloc[0]["Criticita"].split('/')[1]

                        self.__allerta.info_idrogeologico = item.iloc[0]["Idrogeo"].split('/')[0]
                        self.__allerta.allerta_idrogeologico = item.iloc[0]["Idrogeo"].split('/')[1]

                        self.__allerta.info_idraulico = item.iloc[0]["Idraulico"].split('/')[0]
                        self.__allerta.allerta_idraulico = item.iloc[0]["Idraulico"].split('/')[1]

                        self.__allerta.info_temporali = item.iloc[0]["Temporali"].split('/')[0]
                        self.__allerta.allerta_temporali = item.iloc[0]["Temporali"].split('/')[1]

                        self.__allerta.città_interessate = città
                        self.__allerta.nome_file = self.__fileName

                        break

            return self.__allerta