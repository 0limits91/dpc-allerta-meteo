import dpcBollettiniRepositoryParser as dpc
from datetime import date

choise = ("oggi", "domani")
selected_date = date.today()
#selected_date = "2021-08-03"
dpcMeteoParser = dpc.DpcBollettiniRepositoryParser(selected_date)
dpcMeteoParser.choise = choise[0]
dpcMeteoParser.city = "Avellino"
alertResult = dpcMeteoParser.parse()

print(
    "Città: " + alertResult.city + "\n",
    "Zona: " + alertResult.nome_zona + "\n",
    "Info Zona: " + alertResult.info_zona + "\n",
    "Criticità: " + alertResult.allerta_criticità + " - " + alertResult.info_criticità + "\n",
    "Allerta Temporali: " + alertResult.allerta_temporali + " - " + alertResult.info_temporali + "\n",
    "Allerta Idrogeologico: " + alertResult.allerta_idrogeologico + " - " + alertResult.info_idrogeologico + "\n",
    "Allerta Idraulico: " + alertResult.allerta_idraulico + " - " + alertResult.info_temporali + "\n",
    "Comuni Interessati: " + str(alertResult.città_interessate) + "\n",
    "Geometria: " + str(alertResult.geometry)
)