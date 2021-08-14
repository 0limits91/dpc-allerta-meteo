import dpcBollettiniRepositoryParser as dpc
from datetime import date
from tools import formatDateToFilename
from CacheDB import CacheDB
import os

def parseBolletiniMeteo(selected_date, selected_city, choise, usingCache):
    dpcMeteoParser = dpc.DpcBollettiniRepositoryParser(selected_date)
    cacheResult = []
    if usingCache:
        if not os.path.isdir("cache"):
            try:
                os.mkdir("cache")
            except OSError:
                print("Creation of the directory 'cache' failed")

        cache = CacheDB("cache/" + formatDateToFilename(selected_date) + ".db")
        currentFileName = dpcMeteoParser.getRemoteZipFileName(formatDateToFilename(selected_date));
        cacheResult = cache.getReport(f"Select * from cache where nome_file = '{currentFileName.split('_all.zip')[0].split('/')[-1:][0]}' AND city = '{selected_city}' ")

    if len(cacheResult) > 0:
            print("Dati recuperati dalla cache.")
            alertResult = cache.getAlert()
    else:
        print("Cache disabilitata o dati non trovati nella cache!")
        dpcMeteoParser.choise = choise
        dpcMeteoParser.city = selected_city
        alertResult = dpcMeteoParser.parse()
        if usingCache and alertResult.isValid:
            cache.insertReport(selected_date, alertResult)

    return alertResult

def printAlertResult(alertResult):
    if alertResult.isValid:
        print(
            "Città: " + alertResult.city + "\n",
            "Zona: " + alertResult.nome_zona + "\n",
            "Info Zona: " + alertResult.info_zona + "\n",
            "Criticità: " + alertResult.allerta_criticità + " - " + alertResult.info_criticità + "\n",
            "Allerta Temporali: " + alertResult.allerta_temporali + " - " + alertResult.info_temporali + "\n",
            "Allerta Idrogeologico: " + alertResult.allerta_idrogeologico + " - " + alertResult.info_idrogeologico + "\n",
            "Allerta Idraulico: " + alertResult.allerta_idraulico + " - " + alertResult.info_temporali + "\n",
            "Comuni Interessati: " + str(alertResult.città_interessate) + "\n",
            "Geometria: " + str(alertResult.geometry) + "\n",
            "Nome File: " + alertResult.nome_file
        )
    else:
        print("Errore: Risultato non valido!")

if __name__ == '__main__':
    choise = ("oggi", "domani")
    printAlertResult(parseBolletiniMeteo(date.today(), "Avellino", choise[0], usingCache=False))
    printAlertResult(parseBolletiniMeteo("2021-08-03", "Roma", choise[1], usingCache=True))
    printAlertResult(parseBolletiniMeteo(date.today(), "NomeErrato", choise[0], usingCache=True))

