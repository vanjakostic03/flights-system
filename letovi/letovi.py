from datetime import datetime, date, timedelta
import time
import numpy as np

from common import konstante
import csv
import ast

"""
Funkcija koja omogucuje korisniku da pregleda informacije o letovima
Ova funkcija sluzi samo za prikaz
"""
def pregled_nerealizoivanih_letova(svi_letovi: dict):
    lista=[]
    #za main
    for let in svi_letovi.values():
        if let['datum_kraja_operativnosti'] < datetime.now() :
            continue
        
        lista.append(let)
    #za test
    """for let in svi_letovi.values():
        if let['datum_pocetka_operativnosti'] < datetime.now() :
            continue
        
        lista.append(let)"""
    return lista
"""
Funkcija koja omogucava pretragu leta po yadatim kriterijumima. Korisnik moze da zada jedan ili vise kriterijuma.
Povratna vrednost je lista konkretnih letova.
vreme_poletanja i vreme_sletanja su u formatu hh:mm
"""
def pretraga_letova(svi_letovi: dict, konkretni_letovi:dict, polaziste: str = "", odrediste: str = "",
                    datum_polaska: datetime = None, datum_dolaska: datetime = None,
                    vreme_poletanja: str = "", vreme_sletanja: str = "", prevoznik: str = "") -> list:
    lista=[]
    for x in konkretni_letovi:
        konkretan_let=konkretni_letovi[x]       #konkretan_let je instanca konkretnih letova gde je key x
        broj_leta= konkretan_let['broj_leta']   #
        let=svi_letovi[broj_leta]

        if not not polaziste and let['sifra_polazisnog_aerodroma']!=polaziste:
            continue
        elif not not odrediste and let['sifra_odredisnog_aerodorma']!=odrediste:
            continue
        elif not not datum_polaska and konkretan_let['datum_i_vreme_polaska']!=datum_polaska:  #not nad praznim stringom vrati true, not not u tom slucaju vraca false ako je prazan string (isto radi i za none)
            continue
        elif not not datum_dolaska and konkretan_let['datum_i_vreme_dolaska']!=datum_dolaska:
            continue
        elif not not vreme_poletanja and let['vreme_poletanja']!=vreme_poletanja:
            continue
        elif not not vreme_sletanja and let['vreme_sletanja']!=vreme_sletanja:
            continue
        elif prevoznik!="" and let['prevoznik']!=prevoznik:
            continue
        else:
            lista.append(konkretan_let)

    return lista

"""
Funkcija koja trazi 10 najjeftinijih letova po opadajucem redosledu
"""
def trazenje_10_najjeftinijih_letova(svi_letovi: dict, polaziste: str = "", odrediste: str =""):
    sortirana_lista= sorted(svi_letovi.values(), key= lambda x:x['cena'])   #sortirani svi letovi po ceni
    lista=[] #lista koja ce se vratiti
    for x in sortirana_lista:
        if (x.get('sifra_odredisnog_aerodorma')==odrediste or odrediste== "") and (x.get('sifra_polazisnog_aerodroma')==polaziste or polaziste==""):
            lista.append(x)

        if len(lista)== 10:
            break

    return lista

"""
Funkcija koja kreira novi rečnik koji predstavlja let sa prosleđenim vrednostima. Kao rezultat vraća kolekciju
svih letova proširenu novim letom. 
Ova funkcija proverava i validnost podataka o letu. Paziti da kada se kreira let, da se kreiraju i njegovi konkretni letovi.
vreme_poletanja i vreme_sletanja su u formatu hh:mm
CHECKPOINT2: Baca grešku sa porukom ako podaci nisu validni.
"""
def kreiranje_letova(svi_letovi : dict, broj_leta: str, sifra_polazisnog_aerodroma: str,
                     sifra_odredisnog_aerodorma: str,
                     vreme_poletanja: str, vreme_sletanja: str, sletanje_sutra: bool, prevoznik: str,
                     dani: list, model: dict, cena: float,  datum_pocetka_operativnosti: datetime = None ,
                    datum_kraja_operativnosti: datetime = None):
    if broj_leta is None or broj_leta=="":
        raise Exception('Greska, broj leta nije prosledjen')

    if len(broj_leta)!=4:
        raise Exception('Greska, nevalidan broj leta')
    else:
        slova = broj_leta[0:2]
        brojevi = broj_leta[2:]
        if (slova.isalpha()==False or brojevi.isdigit()==False) :
            raise Exception('Greska, nevalidan broj leta')

    if sifra_polazisnog_aerodroma is None or sifra_polazisnog_aerodroma=="":
        raise Exception('Greska, sifra polazisnog aerodroma nije prosledjena')

    if sifra_odredisnog_aerodorma is None or sifra_odredisnog_aerodorma=="":
        raise Exception('Greska, sifra odredisnog aerodroma nije prosledjena')

    if vreme_poletanja is None or vreme_poletanja=="":
        raise Exception('Greska, vreme poletanja nije prosledjeno ')

    if vreme_sletanja is None or vreme_sletanja=="":
        raise Exception('Greska, vreme sletanja nije prosledjeno')

    if sletanje_sutra is None or sletanje_sutra=="":
        raise Exception('Greska')

    if prevoznik is None or prevoznik=="":
        raise Exception('Greska, prevoznik nije prosledjen')

    if len(dani)==0:
        raise Exception('Greska')

    if len(model)==0:
        raise Exception('Greska')
    

    if cena is None or cena==0:
        raise Exception('Greska, cena nije prosledjena')

    if  datum_pocetka_operativnosti=="":
        raise Exception('Greska')

    if  datum_kraja_operativnosti=="":
        raise Exception('Greska')

    
    try:
        datetime.strptime(vreme_poletanja, '%H:%M')
        
    except ValueError:
        raise Exception('nevalidno vreme poletanja')

    try:
        datetime.strptime(vreme_sletanja, '%H:%M')
    except ValueError:
        raise Exception('nevalidno vreme sletanja')

    for i in dani:
        if int(i)<0 or int(i)>6:
            raise Exception('nevalidni dani')
    
    if cena<0: 
        raise Exception('nevalidna cena')

    if model==None:
        raise Exception('model nije prosledjen')

    if datum_pocetka_operativnosti >= datum_kraja_operativnosti:
        raise Exception('Greska, datumi operativnosti')


    novilet = {
        'broj_leta' : broj_leta,
        'sifra_polazisnog_aerodroma' : sifra_polazisnog_aerodroma,
        'sifra_odredisnog_aerodorma' : sifra_odredisnog_aerodorma,
        'vreme_poletanja' : vreme_poletanja,
        'vreme_sletanja' : vreme_sletanja,
        'sletanje_sutra': sletanje_sutra,
        'prevoznik': prevoznik,
        'dani': dani,
        'model': model,
        'cena' : cena,
        'datum_pocetka_operativnosti' : datum_pocetka_operativnosti,
        'datum_kraja_operativnosti': datum_kraja_operativnosti
    }
    svi_letovi[broj_leta]=novilet

    return svi_letovi
"""
Funkcija koja menja let sa prosleđenim vrednostima. Kao rezultat vraća kolekciju
svih letova sa promenjenim letom. 
Ova funkcija proverava i validnost podataka o letu.
vreme_poletanja i vreme_sletanja su u formatu hh:mm
CHECKPOINT2: Baca grešku sa porukom ako podaci nisu validni.
"""
def izmena_letova(
    svi_letovi : dict,
    broj_leta: str,
    sifra_polazisnog_aerodroma: str,
    sifra_odredisnog_aerodorma: str,
    vreme_poletanja: str,
    vreme_sletanja: str,
    sletanje_sutra: bool,
    prevoznik: str,
    dani: list,
    model: dict,
    cena: float,
    datum_pocetka_operativnosti: datetime,
    datum_kraja_operativnosti: datetime
) -> dict:
    
    if isinstance(dani,str):
        dani = ast.literal_eval(dani)

    if broj_leta not in svi_letovi.keys():
        raise Exception ('Greska, nepostojeci let')

    if broj_leta==None:
        raise Exception('Greska, broj leta nije prosledjen')

    if len(broj_leta)!=4:
        raise Exception('Greska, nevalidan broj leta')
    else:
        slova = broj_leta[0:2]
        brojevi = broj_leta[2:]
        if (slova.isalpha()==False or brojevi.isdigit()==False) :
            raise Exception('Greska, nevalidan broj leta')

    if sifra_polazisnog_aerodroma==None or not sifra_polazisnog_aerodroma.isalpha():
        raise Exception('Greska, nije validno polaziste')
    
    if len(sifra_polazisnog_aerodroma)!=3:
        raise Exception('greskaaaa')


    if sifra_odredisnog_aerodorma==None or len(sifra_odredisnog_aerodorma)!=3 or not sifra_odredisnog_aerodorma.isalpha():
        raise Exception('Greska, nije validno odrediste')


    if vreme_poletanja==None:
        raise Exception('Greska, vreme poletanja nije prosledjeno ')

    if vreme_sletanja==None:
        raise Exception('Greska, vreme sletanja nije prosledjeno')

    if prevoznik=="" or prevoznik is None:
        raise Exception('Greska, prevoznik')

    if sletanje_sutra==None:
        raise Exception('Greska')

    if prevoznik==None:
        raise Exception('Greska, prevoznik nije prosledjen')

    if len(dani)==0:
        raise Exception('Greska')

    if model is None or model==0:
        raise Exception('greska')

    if cena is None or cena==0:
        raise Exception('Greska, cena nije prosledjena')

    try:
        datetime.strptime(vreme_poletanja, '%H:%M')
        
    except ValueError:
        raise Exception('nevalidno vreme poletanja')

    try:
        datetime.strptime(vreme_sletanja, '%H:%M')
    except ValueError:
        raise Exception('nevalidno vreme sletanja')

    if datum_pocetka_operativnosti >= datum_kraja_operativnosti:
        raise Exception('Greska, datumi operativnosti')

    
    for i in dani:
        if int(i)<0 or int(i)>6:
            raise Exception('nevalidni dani')
    
    if cena<0: 
        raise Exception('nevalidna cena')

    if model==None:
        raise Exception('model nije prosledjen')

    del svi_letovi[broj_leta]

    novilet = {
        'broj_leta' : broj_leta,
        'sifra_polazisnog_aerodroma' : sifra_polazisnog_aerodroma,
        'sifra_odredisnog_aerodorma' : sifra_odredisnog_aerodorma,
        'vreme_poletanja' : vreme_poletanja,
        'vreme_sletanja' : vreme_sletanja,
        'sletanje_sutra': sletanje_sutra,
        'prevoznik': prevoznik,
        'dani': dani,
        'model': model,
        'cena' : cena,
        'datum_pocetka_operativnosti':datum_pocetka_operativnosti,
        'datum_kraja_operativnosti' : datum_kraja_operativnosti
    }

    print(model)
    svi_letovi[broj_leta]=novilet
    return svi_letovi
"""
Funkcija koja cuva sve letove na zadatoj putanji
"""
def sacuvaj_letove(putanja: str, separator: str, svi_letovi: dict):
    with open(putanja, mode='w') as csv_file:
        polja=['broj_leta','sifra_polazisnog_aerodroma','sifra_odredisnog_aerodorma','vreme_poletanja','vreme_sletanja',
        'sletanje_sutra','prevoznik','dani','model','cena','datum_pocetka_operativnosti','datum_kraja_operativnosti' ]
        writer= csv.DictWriter(csv_file,fieldnames=polja, delimiter=separator)

        writer.writeheader()
        for let in svi_letovi.values():
            writer.writerow(let)

"""
Funkcija koja učitava sve letove iz fajla i vraća ih u rečniku.
"""
def ucitaj_letove_iz_fajla(putanja: str, separator: str) -> dict:
    dict1={ }
    with open(putanja, mode='r') as csv_file:
        csvreader = csv.DictReader(csv_file,delimiter= separator)
        for row in csvreader :
            dict1[row['broj_leta']] ={'broj_leta': row['broj_leta'], 'sifra_polazisnog_aerodroma':row['sifra_polazisnog_aerodroma'],'sifra_odredisnog_aerodorma': row['sifra_odredisnog_aerodorma'], 'vreme_poletanja':row['vreme_poletanja'],'vreme_sletanja':row['vreme_sletanja'],'sletanje_sutra': eval(row['sletanje_sutra']),'prevoznik':row['prevoznik'],'dani':row['dani'],'model':ast.literal_eval(row['model']),'cena':eval(row['cena']),'datum_pocetka_operativnosti':datetime.strptime(row['datum_pocetka_operativnosti'],'%Y-%m-%d %H:%M:%S'), 'datum_kraja_operativnosti':datetime.strptime(row['datum_kraja_operativnosti'],'%Y-%m-%d %H:%M:%S')}


    return dict1

"""
Pomoćna funkcija koja podešava matricu zauzetosti leta tako da sva mesta budu slobodna.
Prolazi kroz sve redove i sve poziciej sedišta i postavlja ih na "nezauzeto".
"""
def podesi_matricu_zauzetosti(svi_letovi: dict, konkretni_let: dict):
    matrica= []

    kljuc= konkretni_let.get('broj_leta')

    if type(svi_letovi[kljuc]['model']['broj_redova']) == str: 
        svi_letovi[kljuc]['model']['broj_redova']=int(svi_letovi[kljuc]['model']['broj_redova'])

    rows = svi_letovi[kljuc]['model']['broj_redova']
    columns= len(svi_letovi[kljuc]['model']['pozicije_sedista'])

    #[True] * 5 = [True, True, True, True, True]
    red= [False]*columns
    matrica = [red]*rows
    konkretni_let['zauzetost']=matrica
    #print(type(matrica))
    return konkretni_let['zauzetost']


"""
Funkcija koja vraća matricu zauzetosti sedišta. Svaka stavka sadrži oznaku pozicije i oznaku reda.
Primer: [[True, False], [False, True]] -> A1 i B2 su zauzeti, A2 i B1 su slobodni
"""
def matrica_zauzetosti(konkretni_let: dict) -> list:
    return konkretni_let.get('zauzetost')


"""
Funkcija koja zauzima sedište na datoj poziciji u redu, najkasnije 48h pre poletanja. Redovi počinju od 1. 
Vraća grešku ako se sedište ne može zauzeti iz bilo kog razloga.
"""
def checkin(karta, svi_letovi: dict, konkretni_let: dict, red: int, pozicija: str) -> (dict, dict):
    broj_leta=konkretni_let['broj_leta']
    let=svi_letovi[broj_leta]

    if red<1:
        raise Exception('Nevalidan broj reda')
    if pozicija.isalpha()==False:
        raise Exception('Nevalidna pozicija')
    if ord(pozicija) > (ord('A')+ len(let['model']['pozicije_sedista'])):
        raise Exception('greska')

    sada=datetime.now()
    datum= konkretni_let['datum_i_vreme_polaska']
    
    promenljiva= timedelta(hours=48)
    delta=datum-sada
    if delta < promenljiva:
        raise Exception('greska, sati')

    matrica=ast.literal_eval( konkretni_let['zauzetost'])
    j= ord(pozicija)-65
    i= red-1

    if matrica[i][j] == True:
        raise Exception('mesto je vec zauzeto')
    else:
        matrica[i][j]=True
        karta['sediste'] = str(red)+pozicija

    karta['status'] = konstante.STATUS_REALIZOVANA_KARTA
    konkretni_let['zauzetost'] = matrica
    return (konkretni_let, karta)


"""
Funkcija koja vraća listu konkretni letova koji zadovoljavaju sledeće uslove:
1. Polazište im je jednako odredištu prosleđenog konkretnog leta
2. Vreme i mesto poletanja im je najviše 120 minuta nakon sletanja konkretnog leta
"""
def povezani_letovi(svi_letovi: dict, svi_konkretni_letovi: dict, konkretni_let: dict) -> list:
    
    lista = []
    broj_leta = konkretni_let['broj_leta']

    for x in svi_konkretni_letovi.values():
        tren = x['broj_leta']               #broj leta trenutnog konkretnog leta
        if svi_letovi[broj_leta]['sifra_odredisnog_aerodorma'] == svi_letovi[tren]['sifra_polazisnog_aerodroma']:
            razlika = x['datum_i_vreme_polaska'] - konkretni_let['datum_i_vreme_dolaska']
            if razlika > timedelta(0) and razlika < timedelta(minutes=120):
                lista.append(x)
            
        

    return lista


"""
Funkcija koja vraća sve konkretne letove čije je vreme polaska u zadatom opsegu, +/- zadati broj fleksibilnih dana
"""
def fleksibilni_polasci(svi_letovi: dict, konkretni_letovi: dict, polaziste: str, odrediste: str,
                        datum_polaska: date, broj_fleksibilnih_dana: int, datum_dolaska: date) -> list:
    def getCena(let):
        return svi_letovi[let['broj_leta']]['cena']

    lista=[]
    pomoc=timedelta(days=int(broj_fleksibilnih_dana))
    datum_polaska = datetime.strptime(datum_polaska, '%Y-%m-%d')
    datum_dolaska = datetime.strptime(datum_dolaska, '%Y-%m-%d')

    for let in konkretni_letovi.values():

        broj_leta=let['broj_leta']
        datum1= datum_polaska-pomoc
        datum2= datum_polaska+pomoc 

        if broj_leta not in svi_letovi:
            continue

        elif polaziste!=svi_letovi[broj_leta]['sifra_polazisnog_aerodroma']:
            continue
        elif odrediste!=svi_letovi[broj_leta]['sifra_odredisnog_aerodorma']:
            continue

        elif let['datum_i_vreme_polaska'] < datum1 or let['datum_i_vreme_polaska']> datum2:
            continue
        else:
            lista.append(let)

    sortirana_lista= sorted(lista, key= getCena)
#sortirana_lista= sorted(svi_letovi.values(), key= lambda x:x['cena'])
    return sortirana_lista