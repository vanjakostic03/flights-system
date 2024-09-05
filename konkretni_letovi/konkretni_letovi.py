from datetime import datetime, timedelta, date 
from letovi import letovi
import csv 
import ast

sledeca_sifra_konkretnog_leta = 1000

"""
Funkcija koja za zadati konkretni let kreira sve konkretne letove u opsegu operativnosti.
Kao rezultat vraća rečnik svih konkretnih letova koji sadrži nove konkretne letove.
"""
def kreiranje_konkretnog_leta(svi_konkretni_letovi: dict, let: dict) -> dict:
    global sledeca_sifra_konkretnog_leta
    
    broj=let['broj_leta']
    pocetak=let['datum_pocetka_operativnosti']
    kraj=let['datum_kraja_operativnosti']
    datum= pocetak
    dani= let['dani']  #['0','1','2','3','4','5','6']


    vreme_poletanja = datetime.strptime(let['vreme_poletanja'],'%H:%M').time()
    vreme_sletanja = datetime.strptime(let['vreme_sletanja'], '%H:%M').time()
    svi_letovi = letovi.ucitaj_letove_iz_fajla('C:\\Users\\Vanja Kostic\\Desktop\\projekat-2022-main\\letovi\\letovi.csv',',')

    
    while datum <= (kraj+ timedelta(days=1)):

        if datum.weekday() in dani:
            #print('Usao je u if prvi')
            #<print(str(datum.weekday()))
            datum_poletanja = datum
            datum_sletanja = datum
            """if let.get('sletanje_sutra') == True:
                datum_sletanja+= timedelta(days=1)"""

            konkretanlet ={
                "sifra": sledeca_sifra_konkretnog_leta,
                "broj_leta": broj,
                "datum_i_vreme_polaska": datetime.combine(datum_poletanja, vreme_poletanja),
                "datum_i_vreme_dolaska": datetime.combine(datum_sletanja, vreme_sletanja)
                
            }


            matrica = letovi.podesi_matricu_zauzetosti(svi_letovi, konkretanlet)
            konkretanlet.update({'zauzetost' : matrica})
            svi_konkretni_letovi[sledeca_sifra_konkretnog_leta]=konkretanlet
            #print(svi_konkretni_letovi)
            sledeca_sifra_konkretnog_leta+=1

        datum += timedelta(days=1)

    return svi_konkretni_letovi


"""
Funkcija čuva konkretne letove u fajl na zadatoj putanji sa zadatim separatorom. 
"""
def sacuvaj_kokretan_let(putanja: str, separator: str, svi_konkretni_letovi: dict):
    with open(putanja, mode='w') as csv_file:
        polja=['sifra','broj_leta','datum_i_vreme_polaska','datum_i_vreme_dolaska','zauzetost']
        writer= csv.DictWriter(csv_file,fieldnames=polja, delimiter=separator)

        writer.writeheader()
        writer.writerows(svi_konkretni_letovi.values())


"""
Funkcija učitava konkretne letove iz fajla na zadatoj putanji sa zadatim separatorom.
"""
def ucitaj_konkretan_let(putanja: str, separator: str) -> dict:
    dict1={ }
    with open(putanja, mode='r') as csv_file:
        csvreader = csv.DictReader(csv_file,delimiter= separator)
        for row in csvreader :
            dict1[int(row['sifra'])] ={'sifra': int(row['sifra']),'broj_leta': row['broj_leta'], 'datum_i_vreme_polaska':datetime.strptime(row['datum_i_vreme_polaska'],'%Y-%m-%d %H:%M:%S'),'datum_i_vreme_dolaska': datetime.strptime(row['datum_i_vreme_dolaska'], '%Y-%m-%d %H:%M:%S'),'zauzetost':row['zauzetost']}

    return dict1
