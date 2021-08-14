import dpcBollettiniRepositoryParser as dpc
from datetime import date
from tools import formatDateToFilename
from CacheDB import CacheDB


choise = ("oggi", "domani")
selected_date = date.today()

#selected_date = "2021-08-03"
db = CacheDB("cache/"+formatDateToFilename(selected_date)+".db")

dpcMeteoParser = dpc.DpcBollettiniRepositoryParser(selected_date)

currentFileName = dpcMeteoParser.getRemoteZipFileName(formatDateToFilename(selected_date));
print(currentFileName.split('_all.zip')[0].split('/')[-1:][0])

rows = db.get("Select * from cache where file_name = '"+currentFileName.split('_all.zip')[0].split('/')[-1:][0]+"'")

if len(rows) > 0:
    for row in rows:
        print("Cached:", row)
        exit(0)
else:
    dpcMeteoParser.choise = choise[0]
    dpcMeteoParser.city = "Avellino"
    alertResult = dpcMeteoParser.parse()
    db.insert(selected_date,alertResult)


print(
    "Città: " + alertResult.city + "\n",
    "Zona: " + alertResult.nome_zona + "\n",
    "Info Zona: " + alertResult.info_zona + "\n",
    "Criticità: " + alertResult.allerta_criticità + " - " + alertResult.info_criticità + "\n",
    "Allerta Temporali: " + alertResult.allerta_temporali + " - " + alertResult.info_temporali + "\n",
    "Allerta Idrogeologico: " + alertResult.allerta_idrogeologico + " - " + alertResult.info_idrogeologico + "\n",
    "Allerta Idraulico: " + alertResult.allerta_idraulico + " - " + alertResult.info_temporali + "\n",
    "Comuni Interessati: " + str(alertResult.città_interessate) + "\n",
    "Geometria: " + str(alertResult.geometry),
    "Nome File: " + alertResult.nome_file
)