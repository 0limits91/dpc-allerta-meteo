#import per scraping
import urllib.request
from bs4 import BeautifulSoup

#import per lettura zip
from io import BytesIO
from zipfile import ZipFile

#import per creazione dataset
import pandas as pandas
from datetime import date, timedelta


def data_formato_link(giorno):
    """ parametro @giorno: ritorna il formato data usato per comporre il link o i nomi dei file dello zip delle criticità """
    oggi = date.today() 
    ieri = oggi - timedelta(days = 1)      

    if(giorno == "oggi"):
        return oggi.strftime('%Y%m%d') #formato AnniMesiGiorni
    
    if(giorno == "ieri"):
       return ieri.strftime('%Y%m%d') #formato AnniMesiGiorni


def applica_filtro_per_data(filtro):
    """ parametro @filtro: ritorna il filtro che contiene parte del link e la data passata come filtro """
    return 'a[href^="/geoserver/bcr/all/'+filtro+'"]'

def estrazione_link_parziale(link, filtro):
    """ parametro @link @filtro: ritorna il link parziale dello zip secondo la data passata come filtro """
    ### estrazione link file zip dal sito ufficiale della protezione civile 
    parser = 'html.parser' 
    risposta = urllib.request.urlopen(link)
    soup = BeautifulSoup(risposta, parser, from_encoding=risposta.info().get_param('charset'))

    return soup.select(filtro)

def zona_from_comune(fileZip, nome_csv_zone, comune):
    with fileZip.open(nome_csv_zone) as data_csv_zone_comuni:
        col_Names=["Zona", "Comune", "Data"]
        data_frame_zone = pandas.read_csv (data_csv_zone_comuni, names = col_Names)
    
    #filtro zona in base al comune selezionato
    zona = data_frame_zone.loc[data_frame_zone['Comune'] == comune]
    return zona.iloc[0]["Zona"]


def allerta_per_zona(fileZip, csv_file_name, zona):
    #lettura file oggi/domani .csv in dataset pandas
    with fileZip.open(csv_file_name) as data_csv:
        data_frame = pandas.read_csv (data_csv)
    return data_frame.loc[data_frame['Zona_all'] == zona]


def allertaPerComune(comune, giorno):
    #Inizializzazione variabili
    base_url = "http://www.protezionecivile.gov.it"
    link_bollettini_criticita = base_url + "/attivita-rischi/meteo-idro/attivita/previsione-prevenzione/centro-funzionale-centrale-rischio-meteo-idrogeologico/previsionale/bollettini-criticita"

    # Costruzione link file zip criticità
    filtro = data_formato_link("oggi")
    link_parziale = estrazione_link_parziale(link_bollettini_criticita, applica_filtro_per_data(filtro))

    # Controllo esistenza file zip nel caso mostro i dati del giorno precedente
    if link_parziale == []:
        filtro = data_formato_link("ieri")
        link_parziale = estrazione_link_parziale(link_bollettini_criticita, applica_filtro_per_data(filtro))
        print("Dati giornalieri non ancora inseriti mostro quelli di ieri")


    # inizializzazione nomi file zip
    link_zip = base_url +  link_parziale[0].attrs['href']
    file_csv_parziale = str(link_parziale[0].attrs['href']).split('_all.zip')[0].split('/')[-1:][0]

   
    ## lettura zip in memoria
    data_zip =  urllib.request.urlopen(link_zip).read()
    fileZip = ZipFile(BytesIO(data_zip))

    # inizializzazione nomi file csv 
    nome_csv_zona = data_formato_link("ieri") + "_ZONE2COMUNI.csv" 
    
    #filtro riga di interesse (ZONA)
    zona = zona_from_comune(fileZip, nome_csv_zona ,comune)

    #filro le allerte per zona
    if(giorno == "domani"):
        nome_csv = file_csv_parziale + "_tomorrow.csv"
    else:
        nome_csv = file_csv_parziale + "_today.csv"
        
    return allerta_per_zona(fileZip,nome_csv,zona)


allerta_oggi = allertaPerComune("Roma", "oggi")

#Stampa delle criticità
print("Oggi")
print("Criticità: " + allerta_oggi.iloc[0]["Criticita"].split('/')[1] + " - " + allerta_oggi.iloc[0]["Criticita"].split('/')[0])
print("Idrogeologico: " + allerta_oggi.iloc[0]["Idrogeo"].split('/')[1] + " - " + allerta_oggi.iloc[0]["Idrogeo"].split('/')[0])
print("Temporali: " + allerta_oggi.iloc[0]["Temporali"].split('/')[1] + " - " + allerta_oggi.iloc[0]["Temporali"].split('/')[0])
print("Idraulico: " + allerta_oggi.iloc[0]["Idraulico"].split('/')[1] + " - " + allerta_oggi.iloc[0]["Idraulico"].split('/')[0])

allerta_domani = allertaPerComune("Roma", "domani")
print("Domani")
print("Criticità: " + allerta_domani.iloc[0]["Criticita"].split('/')[1] + " - " + allerta_domani.iloc[0]["Criticita"].split('/')[0])
print("Idrogeologico: " + allerta_domani.iloc[0]["Idrogeo"].split('/')[1] + " - " + allerta_domani.iloc[0]["Idrogeo"].split('/')[0])
print("Temporali: " + allerta_domani.iloc[0]["Temporali"].split('/')[1] + " - " + allerta_domani.iloc[0]["Temporali"].split('/')[0])
print("Idraulico: " + allerta_domani.iloc[0]["Idraulico"].split('/')[1] + " - " + allerta_domani.iloc[0]["Idraulico"].split('/')[0])