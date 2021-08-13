import io
import json
import requests
import geopandas as gpd
from fiona.io import ZipMemoryFile
from datetime import date, timedelta
from BollettinoMeteo import BollettinoMeteo

class DpcBollettiniRepositoryParser:
    def __init__(self):
        self.__URL = "https://api.github.com/repos/pcm-dpc/DPC-Bollettini-Criticita-Idrogeologica-Idraulica/contents/files/all"
        self.__RAW_URL = "https://raw.githubusercontent.com/pcm-dpc/DPC-Bollettini-Criticita-Idrogeologica-Idraulica/master/files/all"
        self.__day = "oggi"
        self.__city = "Roma"
        self.__jData = json.loads(requests.get(self.__URL).text)

        self.__oggi = date.today()
        self.__ieri = self.__oggi - timedelta(days=1)
        self.__oggi = self.__oggi.strftime('%Y%m%d')
        self.__ieri = self.__ieri.strftime('%Y%m%d')
        self.__zipFileName = ''
        self.__fileName = ''
        self.__allerta = BollettinoMeteo()
    
    @property
    def day(self):
        return self.__day

    @day.setter
    def day(self, day):
        self.__day = day

    @property
    def city(self):
        return self.__city

    @city.setter
    def city(self, city):
        self.__city = city

    def getRemoteZipFileName(self, day_selected):
        for fileInfo in self.__jData:
            if fileInfo['name'].startswith(day_selected):
                return fileInfo['name']
        return ""

    def parse(self):
        if self.__day == "ieri":
            day_selected = self.__ieri
        else:
            day_selected = self.__oggi

        self.__zipFileName = self.getRemoteZipFileName(day_selected)
        if self.__zipFileName == "":
            print("Dati giornalieri non ancora inseriti mostro quelli di ieri/oggi")
            day_selected = self.__ieri
            self.__zipFileName = self.getRemoteZipFileName(day_selected)
            self.day = "domani"

        self.__fileName = self.__zipFileName.split('_all.zip')[0].split('/')[-1:][0]

        # inizializzazione nomi file zip
        link_zip = self.__RAW_URL + '/' + self.__zipFileName

        # lettura zip in memoria
        data_zip = requests.get(link_zip).content
        zipshp = io.BytesIO(data_zip)
        with (ZipMemoryFile(zipshp)) as memfile:
            day_partial_file = "_today"
            if self.__day == "domani":
                day_partial_file = "_tomorrow"

            complete_filename = self.__fileName + day_partial_file + ".shp"
            print(complete_filename)
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
                        self.__allerta.città_interessate = città

                        self.__allerta.info_criticità = item.iloc[0]["Criticita"].split('/')[0]
                        self.__allerta.allerta_criticità= item.iloc[0]["Criticita"].split('/')[1]

                        self.__allerta.info_idrogeologico = item.iloc[0]["Idrogeo"].split('/')[0]
                        self.__allerta.allerta_idrogeologico = item.iloc[0]["Idrogeo"].split('/')[1]

                        self.__allerta.info_idraulico = item.iloc[0]["Idraulico"].split('/')[0]
                        self.__allerta.allerta_idraulico = item.iloc[0]["Idraulico"].split('/')[1]

                        self.__allerta.info_temporali = item.iloc[0]["Temporali"].split('/')[0]
                        self.__allerta.allerta_temporali = item.iloc[0]["Temporali"].split('/')[1]
                        break

            return self.__allerta