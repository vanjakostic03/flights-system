from common import konstante
from functools import reduce
from datetime import datetime, date
import csv

import ast
"""
Brojačka promenljiva koja se automatski povećava pri kreiranju nove karte.
"""
sledeci_broj_karte = 1

"""
Kupovina karte proverava da li prosleđeni konkretni let postoji i da li ima slobodnih mesta. U tom slučaju se karta 
dodaje  u kolekciju svih karata. Slobodna mesta se prosleđuju posebno iako su deo konkretnog leta, zbog lakšeg 
testiranja. Baca grešku ako podaci nisu validni.
kwargs moze da prihvati prodavca kao recnik, i datum_prodaje kao datetime
recnik prodavac moze imati id i ulogu
CHECKPOINT 2: kupuje se samo za ulogovanog korisnika i bez povezanih letova.
ODBRANA: moguće je dodati saputnike i odabrati povezane letove. 
"""
def kupovina_karte(
    sve_karte: dict,
    svi_konkretni_letovi: dict,
    sifra_konkretnog_leta: int,
    putnici: list,
    slobodna_mesta: list,
    kupac: dict,
    **kwargs
) -> (dict, dict):
    
    global sledeci_broj_karte

    if int(sifra_konkretnog_leta) not in svi_konkretni_letovi:
        raise Exception('Greska, izabrali ste nepostojeci let')

    provera= False
    for i in slobodna_mesta:
        if False in i:
            provera=True
        
    if provera == False:
        raise Exception('greska, nema vise slobodnih mesta')

    if kupac['uloga'] != konstante.ULOGA_KORISNIK:
        raise Exception('Greska, samo kupac moze da kupi kartu. ')

    if kwargs.get('prodavac') is not None:
        if kwargs['prodavac']['uloga']!= konstante.ULOGA_PRODAVAC:
            raise Exception('Samo prodavac moze da proda kartu. ')

    datum_prodaje = datetime.now()
    
    nova_karta={
        'broj_karte': sledeci_broj_karte,
        'putnici': putnici,
        'sifra_konkretnog_leta': sifra_konkretnog_leta,
        'status': konstante.STATUS_NEREALIZOVANA_KARTA,
        'obrisana': False,
        'datum_prodaje': datum_prodaje,
        #'datum_prodaje': datetime(year=datum_prodaje.year, month=datum_prodaje.month, day=datum_prodaje.day, hour=datum_prodaje.hour, minute=datum_prodaje.minute, second=datum_prodaje.second),
        'prodavac': kwargs.get('prodavac'),
        'kupac': kupac
        
    }

    sve_karte[sledeci_broj_karte]=nova_karta
    sledeci_broj_karte += 1
    return nova_karta,sve_karte

def pregled_nerealizovanaih_karata(korisnik: dict, sve_karte: iter):

    
    karte=[]
    for x in sve_karte:
        if  korisnik in x['putnici'] and x['status'] == konstante.STATUS_NEREALIZOVANA_KARTA:
            karte.append(x)

    for x in sve_karte:
        if isinstance(x.get('kupac'),str):
            kupac = ast.literal_eval(x.get('kupac'))
        else:
            kupac = x.get('kupac')    #za test
        if korisnik == kupac and x['status'] == konstante.STATUS_NEREALIZOVANA_KARTA:
            karte.append(x)

    
    return karte

"""
Funkcija menja sve vrednosti karte novim vrednostima. Kao rezultat vraća rečnik sa svim kartama, 
koji sada sadrži izmenu.
"""
def izmena_karte(
    sve_karte: iter,
    svi_konkretni_letovi: iter,
    broj_karte: int,
    nova_sifra_konkretnog_leta: int=None,
    nov_datum_polaska: datetime=None,
    sediste=None
) -> dict:

    if broj_karte not in sve_karte:
        raise Exception('Greska, karta ne postoji. ')
    
    karta = sve_karte[broj_karte]
    sifra = karta['sifra_konkretnog_leta']
    karta['sifra_konkretnog_leta'] = nova_sifra_konkretnog_leta

    svi_konkretni_letovi[sifra]['datum_i_vreme_polaska'] = nov_datum_polaska
    karta['sediste'] = sediste
    sve_karte.update({karta['broj_karte'] : karta})

    return sve_karte

"""
 Funkcija brisanja karte se ponaša drugačije u zavisnosti od korisnika:
- Prodavac: karta se označava za brisanje
- Admin/menadžer: karta se trajno briše
Kao rezultat se vraća nova kolekcija svih karata.
"""
def brisanje_karte(korisnik: dict, sve_karte: dict, broj_karte: int) -> dict:

    if broj_karte not in sve_karte:
        raise Exception('Greska, nepostojeca karta')

    else:
        if korisnik.get('uloga')=='prodavac':
            sve_karte[broj_karte]['obrisana']=True
        elif korisnik.get('uloga')=='admin':
            del sve_karte[broj_karte]
        else:
            raise Exception('korisnik ne moze da obrise kartu')

    return sve_karte

"""
Funkcija vraća sve karte koje se poklapaju sa svim zadatim kriterijumima. 
Kriterijum se ne primenjuje ako nije prosleđen.
"""
def pretraga_prodatih_karata(sve_karte: dict, svi_letovi:dict, svi_konkretni_letovi:dict, polaziste: str="",
                             odrediste: str="", datum_polaska: datetime="", datum_dolaska: str="",
                             korisnicko_ime_putnika: str="")->list:

    lista = []
    for x in sve_karte:
        sifra = x['sifra_konkretnog_leta']
        konk_let = svi_konkretni_letovi[sifra]
        broj_leta = konk_let['broj_leta']
        let = svi_letovi[broj_leta]

        if not not polaziste and let['sifra_polazisnog_aerodroma']!=polaziste:
            continue
        elif not not odrediste and let['sifra_odredisnog_aerodorma']!=odrediste:
            continue
        elif not not datum_dolaska and konk_let['datum_i_vreme_dolaska']!=datum_dolaska:
            continue
        elif not not datum_polaska and konk_let['datum_i_vreme_polaska']!=datum_polaska:
            continue
        elif  korisnicko_ime_putnika not in x['putnici']:
            continue
        else:
            lista.append(x)

    return lista

"""
Funkcija čuva sve karte u fajl na zadatoj putanji sa zadatim separatorom.
"""
def sacuvaj_karte(sve_karte: dict, putanja: str, separator: str):
     with open(putanja, mode='w') as csv_file:
        #print('fajl je otvoren')
        polja=['broj_karte', 'sifra_konkretnog_leta', 'kupac', 'prodavac', 'sediste', 'datum_prodaje', 'obrisana', 'status', 'putnici']
        #polja=['broj_karte', 'sifra_konkretnog_leta', 'kupac', 'prodavac', 'sediste', 'datum_prodaje', 'obrisana', 'putnici']
        writer= csv.DictWriter(csv_file,fieldnames=polja, delimiter=separator)
        writer.writeheader()
        for karta in sve_karte.values():
            if isinstance(karta.get('datum_prodaje'), datetime):
                karta['datum_prodaje'].strftime('%d.%m.%Y.')
            writer.writerow(karta)

"""
Funkcija učitava sve karte iz fajla sa zadate putanje sa zadatim separatorom.
"""
def ucitaj_karte_iz_fajla(putanja: str, separator: str) -> dict:
    dict1={ }
    with open(putanja, mode='r') as csv_file:
        csvreader = csv.DictReader(csv_file,delimiter= separator)
        for row in csvreader :
            dict1[ast.literal_eval(row['broj_karte'])]= {'broj_karte':ast.literal_eval( row['broj_karte']), 
            'sifra_konkretnog_leta': ast.literal_eval(row['sifra_konkretnog_leta']),
            'kupac': ast.literal_eval(row['kupac']), 
            'prodavac':row['prodavac'],
            'sediste': row['sediste'], 
            'datum_prodaje':row['datum_prodaje'],
            'obrisana':ast.literal_eval( row['obrisana']),
            'status': row['status'],
            'putnici': ast.literal_eval(row['putnici'])}
            if dict1[ast.literal_eval(row['broj_karte'])]['prodavac'] != "":
                dict1[ast.literal_eval(row['broj_karte'])]['prodavac'] = ast.literal_eval(dict1[ast.literal_eval(row['broj_karte'])]['prodavac'])
            
    return dict1
