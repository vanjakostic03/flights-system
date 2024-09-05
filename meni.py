from sys import exit

import common.konstante
from common import konstante

import aerodromi.aerodromi
from aerodromi import aerodromi

import izvestaji.izvestaji
from izvestaji import izvestaji

import konkretni_letovi.konkretni_letovi
from konkretni_letovi import konkretni_letovi

import korisnici.korisnici
from korisnici import korisnici

import model_aviona.model_aviona
from model_aviona import model_aviona

import letovi.letovi
from letovi import letovi

import karte.karte
from karte import karte

import datetime
from datetime import datetime

import random
import string
from tabulate import tabulate 
import ast

svi_korisnici = {}
svi_letovi = {}
svi_konkretni_letovi = {}
svi_aerodromi = {}
svi_modeli = {}
sve_karte = {}
neregistrovani_korisnici = {}
ulogovan = False   #na pocetku niko nije ulogovan
temp = {}           #trenutno ulogovan korisnik         
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def ucitaj():
    global svi_korisnici
    global svi_aerodromi
    global svi_konkretni_letovi
    global svi_letovi
    global svi_modeli
    global sve_karte
    
    svi_aerodromi= aerodromi.ucitaj_aerodrom('aerodromi/aerodromi.csv', ',')
    svi_modeli = model_aviona.ucitaj_modele_aviona('model_aviona/model_aviona.csv', ',')
    svi_korisnici = korisnici.ucitaj_korisnike_iz_fajla('korisnici/korisnici.csv', ',')
    svi_konkretni_letovi = konkretni_letovi.ucitaj_konkretan_let('konkretni_letovi/konkretni_letovi.csv', ',')
    svi_letovi = letovi.ucitaj_letove_iz_fajla('letovi/letovi.csv', ',')
    sve_karte = karte.ucitaj_karte_iz_fajla('karte/karte.csv', ',')

    try:
        konkretni_letovi.sledeca_sifra_konkretnog_leta = list(svi_konkretni_letovi.keys())[-1] + 1
    except IndexError as E:
        pass
    try:
        karte.sledeci_broj_karte = list(sve_karte.keys())[-1] + 1
    except IndexError as E:
        pass
    try:
        model_aviona.id = list(svi_modeli.keys())[-1] + 1
    except IndexError as E:
        pass

def registracija():
    global svi_korisnici
    global temp
    global ulogovan

    try:
        if ulogovan != False:
            print('Morate prvo da se izlogujete iz trenutnog profila')
            print('------------------------------------------------------------------------------------------------------------------')
        else:
            korisnickoime = input('Unesite korisnicko ime : ')
            lozinka = input('Unesite lozinku : ')
            telefon = input('Unesite kontakt telefon : ')
            email = input('Unesite kontakt email : ')
            ime = input('Unesite vase ime : ')
            prezime = input('Unesite vase prezime : ')
            svi_korisnici = korisnici.kreiraj_korisnika(svi_korisnici, False, konstante.ULOGA_KORISNIK , "", korisnickoime, lozinka, ime, prezime, email, "", "", telefon, "")
            korisnici.sacuvaj_korisnike('korisnici/korisnici.csv',',', svi_korisnici)
            svi_korisnici=korisnici.ucitaj_korisnike_iz_fajla('korisnici/korisnici.csv',',')
            korisnici.login(svi_korisnici, korisnickoime, lozinka)
            pocetnimeni()
    except Exception as E:
        print(E)
        pocetnimeni()

def izlaz():
    exit()

def login():
    global temp
    global svi_korisnici
    global ulogovan
    try:
        if ulogovan == False:
            ime=input('Unesite korisnicko ime : ')
            lozinka=input('Unesite lozinku : ')
            print('------------------------------------------------------------------------------------------------------------------')
            temp = korisnici.login(svi_korisnici,ime,lozinka)
            ulogovan=True
            zajednicki_meni()
        else: 
            print('Morate se prvo izlogovati iz trenutnog profila. ')
            print('------------------------------------------------------------------------------------------------------------------')
            pocetnimeni()
    except Exception as E:
        print(E)
        pocetnimeni()

def logout():
    global temp
    global ulogovan
    if ulogovan == True:
        temp.clear()
        ulogovan=False
        pocetnimeni()
    else:
        print('Morate prvo da se prijavite. ')
        print('------------------------------------------------------------------------------------------------------------------')
        pocetnimeni()
#-------------------------------------------------------------------------ZAJEDNICKE OPCIJE-------------------------------------------------------------------------------------------
def pregled_nerealizovanih_letova():
    global svi_letovi
    lista=[]
    lista=letovi.pregled_nerealizoivanih_letova(svi_letovi)
    polja=[]
    for x in lista[0].keys():
        if x == 'sletanje_sutra' or x == 'dani' or x == 'model' or x == 'datum_pocetka_operativnosti' or x == 'datum_kraja_operativnosti':
            continue
        else:
            polja.append(x)
    redovi=[]
    for x in lista:
        dict1 = {}
        for y in polja:
            dict1.update({ y: x[y]})        #dodajem na dict key sa vrednoscu i kasnije appendujem na listu redovi
        redovi.append(dict1.values())      
    #polja=lista[0].keys()
    #redovi[]
    #redovi=[x.values() for x in lista]
    print(tabulate(redovi, polja, tablefmt='grid'))
    
def pretraga_letova():
    global svi_letovi
    global svi_konkretni_letovi

    print('Pretrazite letove po odgovarajucim kriterijumima (za preskakanje kriterijuma pritisnite enter)')
    polaziste = input('Unesite polazisni aerodrom : ')
    odrediste = input('Unesite odredisni aerodrom : ')
    datum_polaska = input('Unesite datum polaska : ')
    datum_dolaska = input('Unesite datum dolaska : ')
    vreme_poletanja = input('Unesite vreme poletanja : ')
    vreme_sletanja = input('Unesite vreme sletanja : ')
    prevoznik = input('Unesite prevoznika : ')
    
    lista=letovi.pretraga_letova(svi_letovi, svi_konkretni_letovi, polaziste, odrediste, datum_polaska, datum_dolaska, vreme_poletanja, vreme_sletanja, prevoznik)
    if len(lista)==0:
        print('Nema letova za zadate kriterijume. ')
        zajednicki_meni()
    else:
        polja=[]
        for x in lista[0].keys():
            if x == 'zauzetost':
                continue
            else:
                polja.append(x)
        
        redovi=[]
        for x in lista:
            dict1 = {}
            for y in polja:
                dict1.update({ y: x[y]})
            redovi.append(dict1.values())    
        print(tabulate(redovi, polja, tablefmt='grid'))
    
def visekriterijumska_pretraga():
    global svi_letovi
    global svi_konkretni_letovi
    lista=[]

    n = input('Unesite po kom kriterijumu vrsite pretragu\n[1-polazisni aerodrom, 2-odredisni aerodrom, 3-datum polaska, 4-datum dolaska, 5-vreme poletanja, 6-vreme sletanja, 7-prevoznik]: ')

    if int(n) > 7 or int(n) < 1:
        print('Uneli ste nepostojecu opciju. Pretraga neuspesna. ')
        zajednicki_meni()
    else:
        if int(n)==1:
            user_input= input ('Unesite polazisni aerodrom :')
            lista=letovi.pretraga_letova(svi_letovi,svi_konkretni_letovi, user_input, "", "", "", "", "", "")
        elif int(n)==2:
            user_input= input ('Unesite odredisni aerodrom :')
            lista=letovi.pretraga_letova(svi_letovi,svi_konkretni_letovi, "", user_input, "", "", "", "", "")
        elif int(n)==3:
            user_input= input ('Unesite datum i vreme polaska u formatu %Y-%m-%d %H:%M:%S :')
            user_input= datetime.strptime(user_input, '%Y-%m-%d %H:%M:%S')
            lista=letovi.pretraga_letova(svi_letovi,svi_konkretni_letovi, "", "", user_input, "", "", "", "")
        elif int(n)==4:
            user_input= input ('Unesite datum i vreme dolaska u formatu %Y-%m-%d %H:%M:%S :')
            user_input= datetime.strptime(user_input, '%Y-%m-%d %H:%M:%S')
            lista=letovi.pretraga_letova(svi_letovi,svi_konkretni_letovi, "", "", "", user_input, "", "", "")
        elif int(n)==5:
            user_input= input ('Unesite vreme poletanja u formatu HH:MM :')
            lista=letovi.pretraga_letova(svi_letovi,svi_konkretni_letovi, "", "", "", "", user_input, "", "")
        elif int(n)==6:
            user_input= input ('Unesite vreme sletanja u formatu HH:MM:')
            lista=letovi.pretraga_letova(svi_letovi,svi_konkretni_letovi, "", "", "", "", "", user_input, "")
        else:
            user_input= input ('Unesite prevoznika :')
            lista=letovi.pretraga_letova(svi_letovi,svi_konkretni_letovi, "", "", "", "", "", "", user_input)

    if len(lista)==0:
        print('Nema letova za zadat kriterijum. ')
        zajednicki_meni()
    else:
        polja=[]
        for x in lista[0].keys():
            if x == 'zauzetost':
                continue
            else:
                polja.append(x)
        
        redovi=[]
        for x in lista:
            dict1 = {}
            for y in polja:
                dict1.update({ y: x[y]})
            redovi.append(dict1.values())    
        print(tabulate(redovi, polja, tablefmt='grid'))
        
def deset_najjeftinijih():
    global svi_letovi

    polaziste = input('Unesite sifru polazisnog aerodroma : ')
    odrediste = input('Unesite sifru odredisnog aerodroma : ')
    lista=[]
    lista = letovi.trazenje_10_najjeftinijih_letova(svi_letovi, polaziste, odrediste)
    
    polja=[]
    for x in lista[0].keys():
        if x == 'sletanje_sutra' or x == 'dani' or x == 'model' or x == 'datum_pocetka_operativnosti' or x == 'datum_kraja_operativnosti':
            continue
        else:
            polja.append(x)
    redovi=[]
    for x in lista:
        dict1 = {}
        for y in polja:
            dict1.update({ y: x[y]})
        redovi.append(dict1.values())      
    print(tabulate(redovi, polja, tablefmt='grid'))

def fleksibilni_polasci():
    global svi_letovi
    global svi_konkretni_letovi

    polaziste = input('Unesite sifru polazisnog aerodroma : ')
    odrediste = input('Unesite sifru odredisnog aerodroma : ')
    datum_polaska = input('Unesite datum polaska : ')
    datum_dolaska = input('Unesite datum dolaska : ')
    fleksibilni_dani = input('Unesite broj fleksibilnih dana : ')
    lista=[]
    lista= letovi.fleksibilni_polasci(svi_letovi, svi_konkretni_letovi, polaziste, odrediste, datum_polaska, fleksibilni_dani, datum_dolaska)
    if len(lista)==0:
        print('Nema polazaka za zadate kriterijume. ')
        zajednicki_meni()
    else:
        polja=[]
        for x in lista[0].keys():
            if x == 'zauzetost' :
                continue
            else:
                polja.append(x)
    redovi=[]
    for x in lista:
        dict1 = {}
        for y in polja:
            dict1.update({ y: x[y]})
        redovi.append(dict1.values())      
    print(tabulate(redovi, polja, tablefmt='grid'))
#-------------------------------------------------------------------------KORISNIK OPCIJE-------------------------------------------------------------------------------------------
def kupovina_karte():
    global sve_karte
    global svi_konkretni_letovi
    global temp

    n=input('Izaberite nacin kupovine karte [1-Pretraga letova, 2-Unosenje sifre leta] : ')

    if int(n)!= 1 and int(n)!=2:
        print('Izabrali ste nepostojecu opciju. ')
        zajednicki_meni()

    if int(n)==1:
        print(pretraga_letova())
    
    try:
        sifra = input('Unesite sifru leta : ')
        if int(sifra) not in svi_konkretni_letovi:
            print('Uneli ste nepostojeci let. Kupovina je prekinuta. ')
            zajednicki_meni()
        else: 
            putnici = []
            m = int(input('Unesite broj putnika : '))
            if m<1:
                print('Ne mozete kupiti kartu za manje od 1 kupca. Kupovina neuspesna. ')
                zajednicki_meni()

            matrica = eval(letovi.matrica_zauzetosti(svi_konkretni_letovi[int(sifra)]))
            broj_slobodnih_mesta = 0
            for x in matrica:
                for y in x:
                    if y== False:
                        broj_slobodnih_mesta+=1

            if m> broj_slobodnih_mesta:
                print('Nema dovoljno slobodnih mesta. Broj slobodnih mesta je ', str(broj_slobodnih_mesta))
                zajednicki_meni()
            else :
                user_input= input('Unesite DA ako kupujete kartu za sebe : ')
                if user_input.upper() == 'DA':
                    putnik= {'ime': temp['ime'], 'prezime': temp['prezime']}
                    putnici.append(putnik)
                    m-=1
                for i in range(0,m):
                    ime= input('Unesite ime'+str(i+1)+'. saputnika : ')
                    prezime= input('Unesite prezime'+str(i+1)+'. saputnika : ')
                    putnik= {'ime': ime, 'prezime': prezime}
                    putnici.append(putnik)
            
            for x in putnici:
                karta, kartedict = karte.kupovina_karte(sve_karte, svi_konkretni_letovi,sifra,[x],matrica,temp)
                karte.sacuvaj_karte(kartedict,'karte/karte.csv',',')
                sve_karte = karte.ucitaj_karte_iz_fajla('karte/karte.csv',',')
                
            while True:
                user_input = input('Unesite DA ako zelite da kupite jos karata za letove sa odredisnog aerodroma : ')
                if user_input.upper() == 'DA':
                    lista= letovi.povezani_letovi(svi_letovi, svi_konkretni_letovi, svi_konkretni_letovi[int(sifra)])
                    if len(lista)  == 0:
                        print('Nema dostupnih letova. ')
                        zajednicki_meni()
                    
                    else:
                        polja=[]
                        for x in lista[0].keys():
                            if x == 'zauzetost':
                                continue
                            else:
                                polja.append(x)
                        
                        redovi=[]
                        for x in lista:
                            dict1 = {}
                            for y in polja:
                                dict1.update({ y: x[y]})
                            redovi.append(dict1.values())    
                        print(tabulate(redovi, polja, tablefmt='grid'))
                        sifra = input('Unesite sifru sledeceg leta : ')
                        matrica = eval(letovi.matrica_zauzetosti(svi_konkretni_letovi[int(sifra)]))

                        broj_slobodnih_mesta = 0
                        for x in matrica:
                            for y in x:
                                if y == False:
                                    broj_slobodnih_mesta+=1

                        if len(putnici)> broj_slobodnih_mesta:
                            print('Nema dovoljno slobodnih mesta. Broj slobodnih mesta je ', str(broj_slobodnih_mesta))
                            zajednicki_meni()

                        else:
                            for x in putnici:
                                
                                karta, kartedict = karte.kupovina_karte(sve_karte, svi_konkretni_letovi,sifra,[x],matrica,temp)
                                karte.sacuvaj_karte(kartedict,'karte/karte.csv',',')
                                sve_karte = karte.ucitaj_karte_iz_fajla('karte/karte.csv',',')
                else:
                    break
            print('Kupovina uspesno zavrsena. ')
            zajednicki_meni()           
    except ValueError as E:
        print(E)
        zajednicki_meni()
    
def pregled_nerealizovanih_karata():
    global sve_karte
    global temp

    lista=[]
    lista=karte.pregled_nerealizovanaih_karata(temp, sve_karte.values())
    if len(lista) == 0:
        print('Ne postoje nerealizovane karte')
        zajednicki_meni()
    
    polja=[]
    for x in lista[0].keys():
        if x == 'status' or x == 'obrisana' or x == 'prodavac' or x == 'kupac':
            continue
        else:
            polja.append(x)
    
    redovi=[]
    for x in lista:
        dict1 = {}
        for y in polja:
            dict1.update({ y: x[y]})
        redovi.append(dict1.values())    
    
    print(tabulate(redovi, polja, tablefmt='grid'))

def prijava_na_let():
    global sve_karte
    global svi_konkretni_letovi
    global svi_letovi
    global svi_korisnici
    global temp

    nerealizovane_karte = []
    if temp['uloga'] == konstante.ULOGA_KORISNIK:
        ime = temp['ime']
        prezime = temp['prezime']
        for karta in sve_karte.values():
            if ime == karta['putnici'][0]['ime'] and prezime == karta['putnici'][0]['prezime'] and karta['status'] == konstante.STATUS_NEREALIZOVANA_KARTA:
                nerealizovane_karte.append(karta)
    
    if temp['uloga'] == konstante.ULOGA_PRODAVAC:
        for karta in sve_karte.values():
            if karta['status'] == konstante.STATUS_NEREALIZOVANA_KARTA:
                nerealizovane_karte.append(karta)

    if len(nerealizovane_karte) == 0:
        print('Nema karta. ')
        zajednicki_meni()

    polja=[]
    for x in nerealizovane_karte[0].keys():
        if x == 'status' or x == 'obrisana' or x == 'prodavac' or x == 'kupac':
            continue
        else:
            polja.append(x)
    
    redovi=[]
    for x in nerealizovane_karte:
        dict1 = {}
        for y in polja:
            dict1.update({ y: x[y]})
        redovi.append(dict1.values())    
    print(tabulate(redovi, polja, tablefmt='grid'))

    sifra = input('Unesite sifru karte :')
    provera = False
    korisnik = {}
    for x in nerealizovane_karte:
        if int(sifra) == x['broj_karte']:
            provera = True
            if temp['uloga'] == konstante.ULOGA_PRODAVAC:
                ime=x['putnici'][0]['ime']
                prezime=x['putnici'][0]['prezime']
                for i in svi_korisnici.values():
                    if i['ime'] == ime and i['prezime'] == prezime:
                        korisnik = i
                if korisnik == {}:
                    pasos = input('Unesite broj pasosa: ')
                    drzavljanstvo = input('Unesite drzavljanstvo: ')
                    pol = input('Unesite pol: ')
                    while True:
                        korisnicko_ime = ime+prezime+"".join(random.choices(string.digits, k=4))
                        if korisnicko_ime in svi_korisnici:
                            continue
                        else: 
                            break
                    svi_korisnici = korisnici.kreiraj_korisnika(svi_korisnici, False, konstante.ULOGA_KORISNIK, "",korisnicko_ime, "".join(random.choices(string.ascii_lowercase, k=6)), ime, prezime, "", pasos, drzavljanstvo,"",pol)
                    korisnici.sacuvaj_korisnike('korisnici/korisnici.csv',',',svi_korisnici)
                    svi_korisnici = korisnici.ucitaj_korisnike_iz_fajla('korisnici/korisnici.csv',',')
                    korisnik=svi_korisnici[korisnicko_ime]
            if temp['uloga'] == konstante.ULOGA_KORISNIK:
                korisnik = temp
    if provera == False:
        print('izabrali ste nevalidnu kartu. Check in neuspesan')
        zajednicki_meni()
    
    else:   
        izmena = False
        if korisnik['pasos'] == "":
            while True:
                pasos = input('Unesite broj pasosa: ')
                if pasos == "":
                    print('Morate da unesete broj pasosa. ')
                else:
                    izmena = True
                    break
        else: 
            pasos = korisnik['pasos']

        if korisnik['drzavljanstvo'] == "":
            while True:
                drzavljanstvo = input('Unesite drzavljanstvo: ')
                if drzavljanstvo == "":
                    print('Morate uneti drzavljanstvo. ')
                else:
                    izmena = True
                    break
        else: 
            drzavljanstvo = korisnik['drzavljanstvo']

        if korisnik['pol'] == "":
            while True:
                pol = input('Unesite pol: ')
                if pol == "":
                    print('Morate uneti pol. ')
                else:
                    izmena = True
                    break
        else:
            pol = korisnik['pol']     

        if izmena == True:
            dictkorisnici = korisnici.kreiraj_korisnika(svi_korisnici, True, konstante.ULOGA_KORISNIK, korisnik['korisnicko_ime'],korisnik['korisnicko_ime'], korisnik['lozinka'], korisnik['ime'], korisnik['prezime'], korisnik['email'], pasos, drzavljanstvo, korisnik['telefon'], pol) 
            korisnici.sacuvaj_korisnike('korisnici/korisnici.csv',',',dictkorisnici)
            svi_korisnici = korisnici.ucitaj_korisnike_iz_fajla('korisnici/korisnici.csv',',')  
        
        sifra_konkretnog = sve_karte[int(sifra)]['sifra_konkretnog_leta']
        konk_let = svi_konkretni_letovi[sifra_konkretnog]
        broj_leta = konk_let['broj_leta']
        let = svi_letovi[broj_leta]
        kolone_let = len(let['model']['pozicije_sedista'])
        redovi_let = let['model']['broj_redova']
        pozicije = "   "
        for x in let['model']['pozicije_sedista']:
            pozicije += x + " "   
        print(pozicije)
        matrica = ast.literal_eval( konk_let['zauzetost'])
        for x in range(0,redovi_let):
            red=str(x+1) + "."
            if x < 9:
                red+= " "
            for y in range(0,kolone_let):
                if matrica[x][y] == True:
                    red += "X" + " "
                else:
                    red += "_" + " "
            print(red)       
        
        sediste = input('Izaberite sediste oblika <slovo><broj> : ')
        print(sediste[1:0])
        konk_let, sve_karte[int(sifra)] = letovi.checkin(sve_karte[int(sifra)], svi_letovi, konk_let, int(sediste[1:]), sediste[0])
        
        konkretni_letovi.sacuvaj_kokretan_let('konkretni_letovi/konkretni_letovi.csv',',', svi_konkretni_letovi)
        svi_konkretni_letovi = konkretni_letovi.ucitaj_konkretan_let('konkretni_letovi/konkretni_letovi.csv',',')

        karte.sacuvaj_karte(sve_karte,'karte/karte.csv',',')
        sve_karte = karte.ucitaj_karte_iz_fajla('karte/karte.csv',',')
    
        while True:
            povezani = input('Upisite DA da se prijavite na povezani let : ')
            if povezani.upper() != 'DA':
                break

            lista= letovi.povezani_letovi(svi_letovi, svi_konkretni_letovi, konk_let)
            if len(lista)  == 0:
                print('Nema dostupnih letova. ')
                zajednicki_meni()

            nerealizovane_karte = []
            
            for x in lista:
                sifra = x.get('sifra')
                for karta in sve_karte.values():
                    if ime == karta['putnici'][0]['ime'] and prezime == karta['putnici'][0]['prezime'] and karta['status'] == konstante.STATUS_NEREALIZOVANA_KARTA and sifra == karta['sifra_konkretnog_leta']:
                        nerealizovane_karte.append(karta)

            polja=[]
            for x in nerealizovane_karte[0].keys():
                if x == 'kupac' or x == 'prodavac' or x == 'obrisana' or x == 'obrisana':
                    continue
                else:
                    polja.append(x)
            
            redovi=[]
            for x in nerealizovane_karte:
                dict1 = {}
                for y in polja:
                    dict1.update({ y: x[y]})
                redovi.append(dict1.values())    
            tabela=tabulate(redovi, polja, tablefmt='grid')
            print(tabela)
            sifra = input('Unesite sifru karte : ')
            provera = False
            for x in nerealizovane_karte:
                if int(sifra) == x['broj_karte']:
                    provera = True
            
            if provera == False:
                print('izabrali ste nevalidnu kartu. Check in neuspesan')
                zajednicki_meni()
            else:
                sifra_konkretnog = sve_karte[int(sifra)]['sifra_konkretnog_leta']
                konk_let = svi_konkretni_letovi[sifra_konkretnog]
                broj_leta = konk_let['broj_leta']
                let = svi_letovi[broj_leta]
                kolone_let = len(let['model']['pozicije_sedista'])
                redovi_let = let['model']['broj_redova']
                pozicije = "   "
                for x in let['model']['pozicije_sedista']:
                    pozicije += x + " "
                print(pozicije)    
                matrica = ast.literal_eval( konk_let['zauzetost'])
                for x in range(0,redovi_let):
                    red=str(x+1) + "."
                    if x < 9:
                        red+= " "
                    for y in range(0,kolone_let):
                        if matrica[x][y] == True:
                            red += "X" + " "
                        else:
                            red += "_" + " "
                    print(red)       
                
                sediste = input('Izaberite sediste oblika <slovo><broj> : ')
                konk_let, sve_karte[int(sifra)] = letovi.checkin(sve_karte[int(sifra)], svi_letovi, konk_let, int(sediste[1]), sediste[0])
                
                konkretni_letovi.sacuvaj_kokretan_let('konkretni_letovi/konkretni_letovi.csv',',', svi_konkretni_letovi)
                svi_konkretni_letovi = konkretni_letovi.ucitaj_konkretan_let('konkretni_letovi/konkretni_letovi.csv',',')

                karte.sacuvaj_karte(sve_karte,'karte/karte.csv',',')
                sve_karte = karte.ucitaj_karte_iz_fajla('karte/karte.csv',',')
#-------------------------------------------------------------------------PRODAVAC OPCIJE-------------------------------------------------------------------------------------------
def prodaja_karte():
    global svi_korisnici
    global svi_konkretni_letovi
    global sve_karte

    n=input('Izaberite nacin prodaje karte [1-Pretraga letova, 2-Unosenje sifre leta] : ')

    if int(n)!= 1 and int(n)!=2:
        print('Izabrali ste nepostojecu opciju. ')
        zajednicki_meni()

    if int(n)==1:
        print(pretraga_letova())

    sifra = input('Unesite sifru leta : ')
    if int(sifra) not in svi_konkretni_letovi:
        print('Uneli ste nepostojeci let. Prodaja je prekinuta. ')
        zajednicki_meni()
    else: 
        putnici = []
        m = int(input('Unesite broj putnika : '))
        if m<1:
            print('Ne mozete prodati kartu za manje od 1 kupca. Prodaja neuspesna. ')
            zajednicki_meni()

        matrica = eval(letovi.matrica_zauzetosti(svi_konkretni_letovi[int(sifra)]))
        broj_slobodnih_mesta = 0
        for x in matrica:
            for y in x:
                if y== False:
                    broj_slobodnih_mesta+=1

        if m > broj_slobodnih_mesta:
            print('Nema dovoljno slobodnih mesta. Broj slobodnih mesta je ', str(broj_slobodnih_mesta))
            zajednicki_meni()

    for i in range(0,m):
        ime = input('Unesite ime putnika : ')
        prezime = input('Unesite prezime putnika : ')

        nadjen = False
        for x in svi_korisnici.values():
            if x['ime'] == ime and x['prezime'] == prezime:
                nadjen = True
                break       
        kupac= {}
        if nadjen == False:
            telefon = input('Unesite telefon putnika : ')
            email = input('Unesite email putnika : ')
            while True:
                korisnicko_ime=ime+prezime+"".join(random.choices(string.digits, k=4))
                if korisnicko_ime in svi_korisnici:
                    continue
                else:
                    break
            lozinka = "".join(random.choices(string.ascii_lowercase, k=6))
            try:
                dict1=korisnici.kreiraj_korisnika(svi_korisnici, False, 'korisnik', None, korisnicko_ime, lozinka, ime, prezime,email, "", "", telefon, "" )
                korisnici.sacuvaj_korisnike('korisnici/korisnici.csv',',',dict1)
                svi_korisnici = korisnici.ucitaj_korisnike_iz_fajla('korisnici/korisnici.csv',',')
            
            except Exception as E:
                print(E)
                zajednicki_meni()
                
            kupac = list(svi_korisnici.values())[-1]

        else: 
            korisnicko_ime = input('Unesite korisnicko ime putnika : ')
            for x in svi_korisnici.values():
                if x['korisnicko_ime'] == korisnicko_ime:
                    kupac = x
        putnik = []
        putnik.append({'ime' : kupac['ime'], 'prezime' : kupac['prezime']})
        putnici.append({'ime' : kupac['ime'], 'prezime' : kupac['prezime']})
        karta, kartedict =  karte.kupovina_karte(sve_karte, svi_konkretni_letovi, sifra, putnik, matrica, kupac, prodavac = temp  )
        karte.sacuvaj_karte(kartedict,'karte/karte.csv',',')
        sve_karte = karte.ucitaj_karte_iz_fajla('karte/karte.csv',',')
        i+=1
    while True:
        user_input = input('Unesite DA ako zelite da kupite jos karata za letove sa odredisnog aerodroma : ')
        if user_input.upper() == 'DA':
            lista= letovi.povezani_letovi(svi_letovi, svi_konkretni_letovi, svi_konkretni_letovi[int(sifra)])
            if len(lista)  == 0:
                print('Nema dostupnih letova. ')
                zajednicki_meni()
            else:
                polja=[]
                for x in lista[0].keys():
                    if x == 'zauzetost':
                        continue
                    else:
                        polja.append(x)
                
                redovi=[]
                for x in lista:
                    dict1 = {}
                    for y in polja:
                        dict1.update({ y: x[y]})
                    redovi.append(dict1.values())    
                tabela=tabulate(redovi, polja, tablefmt='grid')
                print(tabela)
                sifra = input('Unesite sifru sledeceg leta : ')
                matrica = eval(letovi.matrica_zauzetosti(svi_konkretni_letovi[int(sifra)]))

                broj_slobodnih_mesta = 0
                for x in matrica:
                    for y in x:
                        if y == False:
                            broj_slobodnih_mesta+=1

                if m > broj_slobodnih_mesta:
                    print('Nema dovoljno slobodnih mesta. Broj slobodnih mesta je ', str(broj_slobodnih_mesta))
                    zajednicki_meni()
                else:
                    for x in putnici:
                        for y in svi_korisnici.values():
                            if x['ime'] == y['ime'] and x['prezime'] == y['prezime'] and y['uloga'] == konstante.ULOGA_KORISNIK:
                                kupac = y
                                break
                        karta, kartedict = karte.kupovina_karte(sve_karte, svi_konkretni_letovi,sifra,[x],matrica, kupac,prodavac = temp)
                        karte.sacuvaj_karte(kartedict,'karte/karte.csv',',')
                        sve_karte = karte.ucitaj_karte_iz_fajla('karte/karte.csv',',')
        else:
            break
    print('Kupovina uspesno zavrsena. ')
    zajednicki_meni()

def brisanje_karte_prodavac():
    global sve_karte
    global temp

    n=input('Izaberite nacin brisanja karte [1-Pretraga karata, 2-Unosenje sifre karte] : ')

    if int(n)!= 1 and int(n)!=2:
        print('Izabrali ste nepostojecu opciju. ')
        zajednicki_meni()
    if int(n)==1:
        print(pretraga_prodatih_karata())

    broj = input('Unesite sifru karte : ')
    
    if int(broj) not in sve_karte:
        print('Ne postoji karta sa tim brojem. ')
        zajednicki_meni()

    for x in sve_karte.values():
        if int(broj) == x['broj_karte']:
            x['obrisana'] = True
            break

    karte.sacuvaj_karte(sve_karte,'karte/karte.csv',',')
    sve_karte = karte.ucitaj_karte_iz_fajla('karte/karte.csv',',')

def izmena_karte():
    global sve_karte
    global svi_konkretni_letovi

    n=input('Izaberite nacin izmene karte [1-Pretraga karata, 2-Unosenje sifre karte] : ')

    if int(n)!= 1 and int(n)!=2:
        print('Izabrali ste nepostojecu opciju. ')
        zajednicki_meni()
    if int(n)==1:
        print(pretraga_prodatih_karata())

    broj = int(input('Unesite sifru karte : '))
    
    if int(broj) not in sve_karte:
        print('Ne postoji karta sa tim brojem. ')
        zajednicki_meni()

    nova_sifra = int(input('Unesite novu sifru konkretnog leta : '))
    if nova_sifra not in svi_konkretni_letovi:
        print('Ne postoji let sa tom sifrom. Izmena neuspesna. ')
        zajednicki_meni()

    novo_sediste = input('Izaberite novo sediste : ')
    
    sve_karte = karte.izmena_karte(sve_karte, svi_konkretni_letovi, broj, nova_sifra, None, novo_sediste )
    karte.sacuvaj_karte(sve_karte,'karte/karte.csv',',')
    sve_karte = karte.ucitaj_karte_iz_fajla('karte/karte.csv',',')
#-------------------------------------------------------------------------ADMIN OPCIJE----------------------------------------------------------------------------------------------
def pretraga_prodatih_karata():
    global sve_karte
    global svi_konkretni_letovi
    global svi_letovi

    print('Pritisnite ENTER da preskocite')
    polaziste = input('Unesite sifru polazisnog aerodroma :')
    odrediste = input('Unesite sifru odredisnog aerodroma :')
    polazak = input('Unesite datum polaska u obliku %Y:%m:%d %H:%M:%S : ')
    if polazak !="":
        polazak = datetime.strptime(polazak, '%Y:%m:%d %H:%M:%S')
    dolazak = input('Unesite datum dolaska u obliku %Y:%m:%d %H:%M:%S : ')
    if dolazak !="":
        dolazak = datetime.strptime(dolazak, '%Y:%m:%d %H:%M:%S')
    putnik = input('Unesite DA ako zelite da vrsite pretragu po putniku : ')
    if putnik.upper == 'DA':
        ime = input('Unesite ime putnika : ')
        prezime = input('Unesite prezime putnika : ')
    else:
        ime=""
        prezime = ""

    lista = []
    for x in sve_karte.values():
        sifra = x['sifra_konkretnog_leta']
        konk_let = svi_konkretni_letovi[sifra]
        broj_leta = konk_let['broj_leta']
        let = svi_letovi[broj_leta]

        if polaziste!="" and let['sifra_polazisnog_aerodroma']!= polaziste:
            continue
        elif odrediste!="" and let['sifra_odredisnog_aerodroma']!= odrediste:
            continue
        elif polazak!="" and konk_let['datum_i_vreme_polaska']!= polazak:
            continue
        elif dolazak!="" and konk_let['datum_i_vreme_dolaska']!= dolazak:
            continue
        elif putnik.upper == 'DA' and ime != x['putnici']['ime'] and prezime != x['putnici']['prezime']:
            continue
        else:
            lista.append(x)

    if len(lista) == 0:
        print('Ne postoje karte po datim kriterijumima. ')
        zajednicki_meni()
    
    polja=[]
    for x in lista[0].keys():
        if x == 'status' or x == 'prodavac' or x == 'kupac':
            continue
        else:
            polja.append(x)
    
    redovi=[]
    for x in lista:
        dict1 = {}
        for y in polja:
            dict1.update({ y: x[y]})
        redovi.append(dict1.values())    
    print(tabulate(redovi, polja, tablefmt='grid'))

def unos_leta(azuriraj: bool):
    global svi_letovi
    global svi_konkretni_letovi
    global svi_modeli
    
    broj_leta = input('Unesite broj leta u formatu <slovo><slovo><cifra><cifra>: ')

    if azuriraj == True and broj_leta not in svi_letovi:
        print('Ne postoji let sa datom sifrom. Izmena neuspesna')
        zajednicki_meni()

    while True:
        sifra_polazisnog_aerodroma = input('Unesite sifru polazisnog aerodroma u formatu <slovo><slovo><slovo>: ')
        sifra_odredisnog_aerodorma = input('Unesite sifru odredisnog aerodroma <slovo><slovo><slovo>: ')
        sifra_polazisnog_aerodroma=sifra_polazisnog_aerodroma.upper()
        sifra_odredisnog_aerodorma=sifra_odredisnog_aerodorma.upper()
        if sifra_odredisnog_aerodorma == sifra_polazisnog_aerodroma:
            print("Ne mogu polazisni i odredisni aerodrom da budu isti. Ponovo unesite. ")
            continue
        else:
            break
    
    vreme_poletanja = input('Unesite vreme poletanja u formatu hh:mm: ')
    vreme_sletanja = input('Unesite vreme sletanja u formatu hh:mm: ')

    sletanje_sutra = input('Da li slece sutra? : ')
    if azuriraj == False or (azuriraj == True and sletanje_sutra!= ""):
        sletanje_sutra = sletanje_sutra.upper()
        if sletanje_sutra == 'DA':
            sletanje_sutra = True
        else:
            sletanje_sutra = False

    prevoznik = input('Unesite avio-kompaniju : ')

    lista=['0','1','2','3','4','5','6']
    dani=[]
    n = input('Unesite koliko puta nedeljno saobraca let : ')

    if azuriraj == False or (azuriraj == True and n!= ""):
        if not n.isnumeric:
            print('Niste uneli validnu vrednost. Kreiranje leta neuspesno')
            zajednicki_meni()
        else:
            n=int(n)
            if  n>7 or n<1:
                print('Niste uneli validnu vrednost. Kreiranje leta neuspesno')
                zajednicki_meni()
        
        for i in range(0,n):
            dan = input('Unesite'+ str(i+1) +'.dan [0-6]: ' )
            if dan not in lista:
                print('Uneli ste dan koji ne postoji. Kreiranje leta neuspesno')
                zajednicki_meni()
            else: 
                dani.append(int(dan))

    model = {}
    polja=svi_modeli[0].keys()
    redovi = svi_modeli
    redovi = [[x, *inner.values()] for x, inner in redovi.items()]
    print(tabulate(redovi, polja, tablefmt='grid'))

    print('Izaberite model aviona : ') 
    input_model = input('>>')
    if azuriraj == False or (azuriraj == True and input_model !=""):
        if int(input_model) not in svi_modeli:
            print('Greska, izabrali ste nepostojeci model')
        else: 
            model = svi_modeli[int(input_model)]

    cena = input('Unesite cenu leta : ')
    if azuriraj == False or (azuriraj == True and cena!= ""):
        cena = eval(cena)
    datum_pocetka_operativnosti = input('Unesite datum pocetka operativnosti : ')
    datum_kraja_operativnosti = input('Unesite datum kraja operativnosti : ')

    return (broj_leta, sifra_polazisnog_aerodroma, sifra_odredisnog_aerodorma, vreme_poletanja, vreme_sletanja, sletanje_sutra, prevoznik, dani, model, cena, datum_pocetka_operativnosti, datum_kraja_operativnosti)

def kreiranje_letova():
    global svi_letovi
    global svi_konkretni_letovi
    global svi_modeli

    broj_leta, sifra_polazisnog_aerodroma, sifra_odredisnog_aerodorma, vreme_poletanja, vreme_sletanja, sletanje_sutra, prevoznik, dani, model, cena, datum_pocetka_operativnosti, datum_kraja_operativnosti = unos_leta(False)
    try:     
            letovidict=letovi.kreiranje_letova(svi_letovi, broj_leta, sifra_polazisnog_aerodroma, sifra_odredisnog_aerodorma, vreme_poletanja, vreme_sletanja, sletanje_sutra, prevoznik, dani, model, cena, datum_pocetka_operativnosti, datum_kraja_operativnosti)
            letovi.sacuvaj_letove('letovi/letovi.csv',',',letovidict)
            svi_letovi= letovi.ucitaj_letove_iz_fajla('letovi/letovi.csv',',')

            let={ 'broj_leta' : broj_leta,'sifra_polazisnog_aerodroma' : sifra_polazisnog_aerodroma,'sifra_odredisnog_aerodorma' : sifra_odredisnog_aerodorma,
                 'vreme_poletanja' : vreme_poletanja,'vreme_sletanja' : vreme_sletanja,'sletanje_sutra': sletanje_sutra,'prevoznik': prevoznik,'dani': dani,'model': model,
                 'cena' : cena,'datum_pocetka_operativnosti': datetime.strptime(datum_pocetka_operativnosti, '%Y-%m-%d %H:%M:%S'),
                 'datum_kraja_operativnosti': datetime.strptime(datum_kraja_operativnosti, '%Y-%m-%d %H:%M:%S')}

            kletovidict=konkretni_letovi.kreiranje_konkretnog_leta(svi_konkretni_letovi, let)
            konkretni_letovi.sacuvaj_kokretan_let('konkretni_letovi/konkretni_letovi.csv',',',kletovidict)
            svi_konkretni_letovi= konkretni_letovi.ucitaj_konkretan_let('konkretni_letovi/konkretni_letovi.csv',',')

    except ValueError as E:
        print('upao u exception')
        print(E)
        zajednicki_meni()

def izmena_leta():    
    global svi_letovi
    global svi_konkretni_letovi
    global svi_modeli

    broj_leta, sifra_polazisnog_aerodroma, sifra_odredisnog_aerodorma, vreme_poletanja, vreme_sletanja, sletanje_sutra, prevoznik, dani, model, cena, datum_pocetka_operativnosti, datum_kraja_operativnosti = unos_leta(True)
    
    let=svi_letovi[broj_leta]

    if sifra_polazisnog_aerodroma == "":
        sifra_polazisnog_aerodroma=let['sifra_polazisnog_aerodroma']

    if sifra_odredisnog_aerodorma == "":
        sifra_odredisnog_aerodorma=let['sifra_odredisnog_aerodorma']

    if vreme_sletanja == "":
        vreme_sletanja=let['vreme_sletanja']

    if vreme_poletanja == "":
        vreme_poletanja=let['vreme_poletanja']

    if sletanje_sutra == "":
        sletanje_sutra=let['sletanje_sutra']

    if prevoznik == "":
        prevoznik=let['prevoznik']

    if dani == []:
        dani=let['dani']

    if model == {}:
        model = let['model']
    
    if cena == "":
        cena=let['cena']

    if datum_pocetka_operativnosti == "":
        datum_pocetka_operativnosti=let['datum_pocetka_operativnosti']

    if datum_kraja_operativnosti == "":
        datum_kraja_operativnosti=let['datum_kraja_operativnosti']

    letovidict =letovi.izmena_letova(svi_letovi, broj_leta,sifra_polazisnog_aerodroma, sifra_odredisnog_aerodorma,vreme_poletanja, vreme_sletanja, sletanje_sutra, prevoznik, dani, model, cena, datum_pocetka_operativnosti, datum_kraja_operativnosti )
    letovi.sacuvaj_letove('letovi/letovi.csv',',',letovidict)
    svi_letovi= letovi.ucitaj_letove_iz_fajla('letovi/letovi.csv',',')

    let={ 'broj_leta' : broj_leta,
            'sifra_polazisnog_aerodroma' : sifra_polazisnog_aerodroma,
            'sifra_odredisnog_aerodorma' : sifra_odredisnog_aerodorma,
            'vreme_poletanja' : vreme_poletanja,
            'vreme_sletanja' : vreme_sletanja,
            'sletanje_sutra': sletanje_sutra,
            'prevoznik': prevoznik,
            'dani': ast.literal_eval(dani),
            'model': model,
            'cena' : cena,
            'datum_pocetka_operativnosti': datum_pocetka_operativnosti,
            'datum_kraja_operativnosti': datum_kraja_operativnosti}

    kletovidict=konkretni_letovi.kreiranje_konkretnog_leta(svi_konkretni_letovi, let)
    konkretni_letovi.sacuvaj_kokretan_let('konkretni_letovi/konkretni_letovi.csv',',',kletovidict)
    svi_konkretni_letovi= konkretni_letovi.ucitaj_konkretan_let('konkretni_letovi/konkretni_letovi.csv',',')

def brisanje_karata_admin():
    global temp
    global sve_karte

    print('Karte za brisanje : ')
    lista = []
    for x in sve_karte.values():
        if x['obrisana'] == True:
            lista.append(x)

    if len(lista) == 0:
        print('Nema karata za brisanje. ')
        zajednicki_meni()

    polja=[]
    for x in lista[0].keys():
        if x == 'status' or x == 'prodavac' or x == 'kupac':
            continue
        else:
            polja.append(x)
    
    redovi=[]
    for x in lista:
        dict1 = {}
        for y in polja:
            dict1.update({ y: x[y]})
        redovi.append(dict1.values())    
    print(tabulate(redovi, polja, tablefmt='grid'))

    n = input('Izaberite opciju [1-brisanje, 2-ponistavanje brisanja] : ')
    if int(n) == 1:
        opcija = input('Izaberite opciju [1-brisanje svih karata, 2-brisanje odredjenih karata] : ')
        if int(opcija) != 1 and int(opcija) != 2:
            print('Nepostojeca opcija. Brisanje neuspesno. ')
            zajednicki_meni()

        if int(opcija) == 2:
            lista = []
            print('Za kraj pritisnite enter')
            while True:
                user_input = input('Unesite broj karte za brisanje : ')
                if user_input == "":
                    break
                else:
                    lista.append(sve_karte[int(user_input)])
        
        for x in lista:
            broj_karte = x['broj_karte']
            karte.brisanje_karte(temp, sve_karte, broj_karte)
    elif int(n) == 2:
        opcija = input('Izaberite opciju [1-ponistavanje brisanja svih karata, 2-ponistavanje brisanja odredjenih karata] : ')
        if int(opcija) != 1 and int(opcija) != 2:
            print('Nepostojeca opcija. Brisanje neuspesno. ')
            zajednicki_meni()

        if int(opcija) == 2:
            lista = []
            print('Za kraj pritisnite enter')
            while True:
                user_input = input('Unesite broj karte za ponistavanje brisanja : ')
                if user_input == "":
                    break
                else:
                    lista.append(sve_karte[int(user_input)])
        
        for x in lista:
            x['obrisana'] = False
    else:
        print('Nepostojeca opcija. Brisanje neuspesno. ')
        zajednicki_meni()       

    karte.sacuvaj_karte(sve_karte,'karte/karte.csv',',')
    sve_karte = karte.ucitaj_karte_iz_fajla('karte/karte.csv',',')

def registracija_prodavca():
    global svi_korisnici
    try:
        korisnicko_ime = input('Unesite korisnicko ime novog prodavca : ')
        lozinka = input('Unesite lozinku novog prodavca : ')
        ime = input('Unesite ime novog prodavca : ')
        prezime = input('Unesite prezime novog prodavca : ')
        email = input('Unesite email novog prodavca : ')
        pasos = input('Unesite pasos novog prodavca : ')
        drzavljanstvo = input('Unesite drzavljanstvo novog prodavca : ')
        telefon = input('Unesite telefon novog prodavca : ')
        pol = input('Unesite pol novog prodavca : ')
        korisnicidict=korisnici.kreiraj_korisnika(svi_korisnici, False, konstante.ULOGA_PRODAVAC, "", korisnicko_ime, lozinka, ime, prezime, email, pasos, drzavljanstvo, telefon, pol)
        korisnici.sacuvaj_korisnike('korisnici/korisnici.csv',',', korisnicidict)
        svi_korisnici=korisnici.ucitaj_korisnike_iz_fajla('korisnici/korisnici.csv',',')
    except Exception as E:
        print(E)
        zajednicki_meni()

def izvestaji_admin():
    def ispistabele(lista : list):
        if len(lista) == 0:
            print('Nema izvestaja')
            zajednicki_meni()

        polja=[]
        for x in lista[0].keys():
            if x == 'status' or x == 'prodavac' or x == 'kupac':
                continue
            else:
                polja.append(x)

        redovi=[]
        for x in lista:
            dict1 = {}
            for y in polja:
                dict1.update({ y: x[y]})
            redovi.append(dict1.values())    
        print(tabulate(redovi, polja, tablefmt='grid'))
    global sve_karte
    global svi_konkretni_letovi
    global svi_letovi

    print('1. Prodaja karata za dan prodaje')
    print('2. Prodaja karata za dan polaska')
    print('3. Prodaja karata za dan prodaje i prodavca')
    print('4. Prodaja karata za dan prodaje (ukupan broj i cena)')
    print('5. Prodaja karata za dan polaska (ukupan broj i cena)')
    print('6. Prodaja karata za dan prodaje i prodavca (ukupan broj i cena)')
    print('7. Prodaja karata u poslednjih 30 dana po prodavcu (ukupan broj i cena)')
    opcija = int(input('>>'))
    if opcija<1 or opcija>7:
        print('Izabrali ste nepostojecu opciju. ')
        zajednicki_meni()

    if opcija == 1:
        datum_input = input('Unesite datum prodaje u formatu d.m.y. : ')
        datum = datetime.strptime(datum_input, '%d.%m.%Y.')
        lista=izvestaji.izvestaj_prodatih_karata_za_dan_prodaje(sve_karte, datum)
        ispistabele(lista)

    if opcija == 2:
        datum = input('Unesite datum polaska u formatu y-m-d : ')
        datum = datetime.strptime(datum, '%Y-%m-%d')
        lista= izvestaji.izvestaj_prodatih_karata_za_dan_polaska(sve_karte, svi_konkretni_letovi, datum)
        ispistabele(lista)

    if opcija == 3:
        datum_input = input('Unesite datum prodaje u formatu d.m.y. : ')
        datum = datetime.strptime(datum_input, '%d.%m.%Y.')
        prodavac_input = input('Unesite korisnicko ime prodavca. ')
        lista = izvestaji.izvestaj_prodatih_karata_za_dan_prodaje_i_prodavca(sve_karte,datum, prodavac_input)
        ispistabele(lista)

    if opcija == 4:
        datum_input = input('Unesite datum prodaje u formatu d.m.y. : ')
        datum = datetime.strptime(datum_input, '%d.%m.%Y.')
        (broj, suma) = izvestaji.izvestaj_ubc_prodatih_karata_za_dan_prodaje(sve_karte, svi_konkretni_letovi, svi_letovi, datum)
        print('Broj prodatih karata : ', broj)
        print('Suma novca prodatih karata : ', suma)

    if opcija == 5:
        datum = input('Unesite datum polaska u formatu y-m-d : ')
        datum = datetime.strptime(datum, '%Y-%m-%d')
        (broj, suma) = izvestaji.izvestaj_ubc_prodatih_karata_za_dan_polaska(sve_karte, svi_konkretni_letovi, svi_letovi, datum)
        print('Broj prodatih karata : ', broj)
        print('Suma novca prodatih karata : ', suma)
    
    if opcija == 6:
        datum_input = input('Unesite datum prodaje u formatu d.m.y. : ')
        datum = datetime.strptime(datum_input, '%d.%m.%Y.')
        prodavac_input = input('Unesite korisnicko ime prodavca. ')
        (broj, suma) = izvestaji.izvestaj_ubc_prodatih_karata_za_dan_prodaje_i_prodavca(sve_karte, svi_konkretni_letovi, svi_letovi, datum, prodavac_input)
        print('Broj prodatih karata : ', broj)
        print('Suma novca prodatih karata : ', suma)
    if opcija == 7:
        dict = izvestaji.izvestaj_ubc_prodatih_karata_30_dana_po_prodavcima(sve_karte, svi_konkretni_letovi, svi_letovi)
        if dict == {}:
            print("Nema izvestaja. ")
            zajednicki_meni()
        else:
            polja = ['broj_karata', 'cena' , 'korisnicko_ime' ]
            redovi = []
            for x in dict.values():
                redovi.append(x)
            print(tabulate(redovi, polja, tablefmt="grid"))
#-------------------------------------------------------------------------SVI MENIJI-------------------------------------------------------------------------------------------
def zajednicki_meni():
    global temp
    global ulogovan
    
    glavni_dict={
        '1': pregled_nerealizovanih_letova,
        '2': pretraga_letova,
        '3': visekriterijumska_pretraga,
        '4': deset_najjeftinijih,
        '5': fleksibilni_polasci
    }
    tekst= '1. Pregled nerealizovanih letova\n2. Pretraga letova\n3. Visekriterijumska pretraga letova\n4. Prikaz 10 najjeftinijih letova\n5. Fleksibilni polasci\n'

    if temp.get('uloga')!=None:
        if temp['uloga']=='korisnik':
            glavni_dict.update({'6': kupovina_karte})
            glavni_dict.update({'7': pregled_nerealizovanih_karata})
            glavni_dict.update({'8': prijava_na_let})
            
            tekst+='6. Kupovina karata\n7. Pregled nerealizovanih karata\n8. Prijava na let (check in)\n'

        if temp['uloga'] =='prodavac': 
            glavni_dict.update({'6': prodaja_karte})
            glavni_dict.update({'7': prijava_na_let})
            glavni_dict.update({'8': izmena_karte})
            glavni_dict.update({'9': brisanje_karte_prodavac})
            glavni_dict.update({'10': pretraga_prodatih_karata})

            tekst+='6. Prodaja karata\n7. Prijava na let\n8. Izmena karte\n9. Brisanje karata\n10. Pretraga prodatih karata\n'

        if temp['uloga'] == 'admin':
            glavni_dict.update({'6': pretraga_prodatih_karata})
            glavni_dict.update({'7': registracija_prodavca})
            glavni_dict.update({'8': kreiranje_letova})
            glavni_dict.update({'9': izmena_leta})
            glavni_dict.update({'10': brisanje_karata_admin})
            glavni_dict.update({'11': izvestaji_admin})

            tekst+='6. Pretraga prodatih karata\n7. Registracija novih prodavaca\n8. Kreiranje letova\n9. Izmena letova\n10. Brisanje karata\n11. Izvestaji\n'
        
    glavni_dict.update({'<' : pocetnimeni})
    tekst+= '<. Nazad'

    while True:

        print('Ponuđene opcije:')
        print(tekst)

        user_input = input('>>')

        if user_input in glavni_dict:
            glavni_dict[user_input]()
            if user_input == '<':
                return
        else:
            print('Odabrali ste nepostojeću opciju')

def pocetnimeni():
    global sve_karte
    ucitaj()
    pmenidict={
        '1': login,
        '2': zajednicki_meni,
        '3': registracija,
        '4': logout,
        'x': izlaz
    }

    while True:
        print('Ponuđene opcije:')
        print('1. Prijava na sistem\n2. Prikaz glavnog menija\n3. Registracija korisnika\n4. Odjava sa sistema\nx. Izlazak iz aplikacije\n')

        user_input = input('>>')

        if user_input in pmenidict:
            pmenidict[user_input]()
            if user_input == 'x':
                return
        else:
            print('Odabrali ste nepostojeću opciju')
