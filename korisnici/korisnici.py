import sys
sys.path.insert(1,'C:\\Users\\Vanja Kostic\\faks\\prvi semestar\\osnove programiranje\\cp2\\projekat-2022-main') 


import common.konstante
from common import konstante
import csv

"""
Funkcija koja kreira novi rečnik koji predstavlja korisnika sa prosleđenim vrednostima. Kao rezultat vraća kolekciju
svih korisnika proširenu novim korisnikom. Može se ponašati kao dodavanje ili ažuriranje, u zavisnosti od vrednosti
parametra azuriraj:
- azuriraj == False: kreira se novi korisnik. staro_korisnicko_ime ne mora biti prosleđeno.
Vraća grešku ako korisničko ime već postoji.
- azuriraj == True: ažurira se postojeći korisnik. Staro korisnicko ime mora biti prosleđeno. 
Vraća grešku ako korisničko ime ne postoji.

Ova funkcija proverava i validnost podataka o korisniku, koji su tipa string.

CHECKPOINT 1: Vraća string sa greškom ako podaci nisu validni.
    Hint: Postoji string funkcija koja proverava da li je string broj bez bacanja grešaka. Probajte da je pronađete.
ODBRANA: Baca grešku sa porukom ako podaci nisu validni.
"""
def kreiraj_korisnika(svi_korisnici: dict, azuriraj: bool, uloga: str, staro_korisnicko_ime: str, 
                      korisnicko_ime: str, lozinka: str, ime: str, prezime: str, email: str = "",
                      pasos: str = "", drzavljanstvo: str = "",
                      telefon: str = "", pol: str = "") -> dict:
   #provere: 

    if azuriraj is None:
        raise Exception('greska')

    if korisnicko_ime is None:
        raise Exception('greska')

    if uloga is None:
        raise Exception('greska')

    if uloga!='korisnik' and uloga!='admin' and uloga!='prodavac':  
        raise Exception('greska,nepostojeca uloga')


    if lozinka is None:
        raise Exception('greska')

    if ime is None:
        raise Exception('greska')

    if prezime is None:
        raise Exception('greska')

    if email!="":
        if email is None:
            raise Exception('greska, mail nije prosledjen')

        elif '@' not in email:
            raise Exception('greska, nevalidan mail')

        else:
            i=email.find('@')   #i je index na kom se nalazi @
            j=len(email)-1      #j je broj elemenata u stringu
            domen=email[i:j]    # domen je string koji je podstring email (od @ do kraja stringa)
            broj=0
            for k in domen:
                if k=='.':
                    broj+=1
            
            if broj != 1:     #ako postoji vise tacaka onda nije validno
                raise Exception('greska, nevalidan domen')



    if pasos is None:
        raise Exception('greska, broj pasosa nije prosledjen ')

    if pasos !="":
        if pasos is not None:
            #pasos=str(pasos)
            if pasos!="":
                if pasos.isdigit()!= True:
                    raise Exception('greska, nevalidan broj pasosa')

                if len(pasos)!= 9:
                    raise Exception('greska, nevalidan broj cifara')

    if drzavljanstvo is None:
        raise Exception ('greska')

    if telefon is None:
        raise Exception('greska, broj nije prosledjen')

    if telefon!="":
        if telefon.isdigit()!= True:
            raise Exception('greska, nevalidan broj telefona')

    if pol is None:
        raise Exception ('greska')

    
    


    if azuriraj == False:

        if korisnicko_ime in svi_korisnici.keys():
            raise Exception('greska, korisnicko ime vec postoji')
          

        novikorisnik = {

            'korisnicko_ime' : korisnicko_ime,
            'lozinka' : lozinka,
            'ime' : ime,
            'prezime' : prezime, 
            'uloga' : uloga,
            'email': email,
            'pasos': pasos,
            'drzavljanstvo' : drzavljanstvo,
            'telefon' : telefon,
            'pol': pol
        }
        svi_korisnici[korisnicko_ime] = novikorisnik
        print('dodat je novi korisnik')

    else :
        
        if staro_korisnicko_ime == None:
            raise Exception ('Greska, niste uneli staro k ime')

        elif staro_korisnicko_ime not in svi_korisnici.keys():
            raise Exception ('greska, korisnicko ime ne postoji')

        elif korisnicko_ime!=staro_korisnicko_ime :
            if korisnicko_ime in  svi_korisnici.keys():
               raise Exception( 'greska, takvo korisnicko ime vec postoji')
         
        del svi_korisnici[staro_korisnicko_ime]
        novikorisnik = {

            'korisnicko_ime' : korisnicko_ime,
            'lozinka' : lozinka,
            'ime' : ime,
            'prezime' : prezime, 
            'uloga' : uloga,
            'email': email,
            'pasos': pasos,
            'drzavljanstvo' : drzavljanstvo,
            'telefon' : telefon,
            'pol': pol
        }

        svi_korisnici[korisnicko_ime] = novikorisnik

        print('azuriran je korsnik')

    return svi_korisnici

"""
Funkcija koja čuva podatke o svim korisnicima u fajl na zadatoj putanji sa zadatim separatorom.
"""
def sacuvaj_korisnike(putanja: str, separator: str, svi_korisnici: dict):
    with open(putanja, mode='w') as csv_file:
        polja=['korisnicko_ime','lozinka','ime','prezime','uloga','email','pasos','drzavljanstvo','telefon','pol']
        writer= csv.DictWriter(csv_file,fieldnames=polja, delimiter=separator)

        writer.writeheader()
        writer.writerows(svi_korisnici.values())


"""
Funkcija koja učitava sve korisnika iz fajla na putanji sa zadatim separatorom. Kao rezultat vraća učitane korisnike.
"""
def ucitaj_korisnike_iz_fajla(putanja: str, separator: str) -> dict:
    dict1={ }
    with open(putanja, mode='r') as csv_file:
        csvreader = csv.DictReader(csv_file,delimiter= separator)
        for row in csvreader :
            dict1[row['korisnicko_ime']] ={'korisnicko_ime': row['korisnicko_ime'], 'lozinka':row['lozinka'],'ime': row['ime'], 'prezime':row['prezime'],'uloga':row['uloga'],'email':row['email'],'pasos':row['pasos'],'drzavljanstvo':row['drzavljanstvo'],'telefon':row['telefon'],'pol':row['pol'] }


    return dict1


"""
Funkcija koja vraća korisnika sa zadatim korisničkim imenom i šifrom.
CHECKPOINT 1: Vraća string sa greškom ako korisnik nije pronađen.
ODBRANA: Baca grešku sa porukom ako korisnik nije pronađen.
"""
def login(svi_korisnici, korisnicko_ime, lozinka) -> dict:
    
    lista = []
    for x in svi_korisnici:
        lista.append(x)

    if korisnicko_ime not in lista:
        raise Exception('Greska, ne postoji korisnicko ime')

    elif svi_korisnici[korisnicko_ime]['lozinka'] == lozinka:
        return svi_korisnici[korisnicko_ime]
    else:
        raise Exception('Greska, pogresna lozinka')

"""
Funkcija koja vrsi log out
*
"""
def logout(korisnicko_ime: str):
    pass

