from datetime import datetime, date, timedelta
import ast
"""
Funkcija kao rezultat vraća listu karata prodatih na zadati dan.
"""
def provera (datum):
    if isinstance(datum, str):
        datum = datetime.strptime(datum, '%Y-%m-%d %H:%M:%S.%f')
    return datum

def proveraprodavac (prodavac):
    return prodavac['korisnicko_ime']

def izvestaj_prodatih_karata_za_dan_prodaje(sve_karte: dict, dan: date) -> list:
    lista=[]
    #prolazi test
    """for x in sve_karte.values():
        if x['datum_prodaje']!=dan:
            continue
        else:
            lista.append(x)"""
    #prolazi meni
    for x in sve_karte.values():
        x['datum_prodaje']=provera(x['datum_prodaje'])
        if x['datum_prodaje'].day!=dan.day or x['datum_prodaje'].month!=dan.month or x['datum_prodaje'].year!=dan.year:
            continue
        else:
            lista.append(x)
    return lista

"""
Funkcija kao rezultat vraća listu svih karata čiji je dan polaska leta na zadati dan.
"""
def izvestaj_prodatih_karata_za_dan_polaska(sve_karte: dict, svi_konkretni_letovi: dict, dan: date) -> list:
    lista=[]
    #prolazi test
    """for x in sve_karte.values():
        sifra=x['sifra_konkretnog_leta']
        if svi_konkretni_letovi[sifra]['datum_i_vreme_polaska'].day != dan.day:
            continue
        else:
            lista.append(x)"""

    #prolazi meni
    for x in sve_karte.values():
        sifra=x['sifra_konkretnog_leta']
        if svi_konkretni_letovi[sifra]['datum_i_vreme_polaska'].day != dan.day or svi_konkretni_letovi[sifra]['datum_i_vreme_polaska'].month != dan.month or svi_konkretni_letovi[sifra]['datum_i_vreme_polaska'].year != dan.year:
            continue
        else:
            lista.append(x)

    return lista

"""
Funkcija kao rezultat vraća listu karata koje je na zadati dan prodao zadati prodavac.
"""
def izvestaj_prodatih_karata_za_dan_prodaje_i_prodavca(sve_karte: dict, dan: date, prodavac: str) -> list:
    lista=[]
    #prolazi test
    """for x in sve_karte.values():
            if x['prodavac'] != prodavac:
                continue
            elif x['datum_prodaje'] != dan:
                continue    
            else:
                lista.append(x)"""
    #prolazi meni
    for x in sve_karte.values():
        x['datum_prodaje']=provera(x['datum_prodaje'])
        if not x['prodavac']:
            continue
        if isinstance(x['prodavac'], dict):
            if x['prodavac'].get('korisnicko_ime') != prodavac:
                continue
            elif x['datum_prodaje'].day!=dan.day or x['datum_prodaje'].month!=dan.month or x['datum_prodaje'].year!=dan.year:
                continue    
            else:
                lista.append(x)
        else:
            if x['datum_prodaje'] == dan and x['prodavac'] == prodavac:
                lista.append(x)
    return lista

"""
Funkcija kao rezultat vraća dve vrednosti: broj karata prodatih na zadati dan i njihovu ukupnu cenu.
Rezultat se vraća kao torka. Npr. return broj, suma
"""
def izvestaj_ubc_prodatih_karata_za_dan_prodaje(
    sve_karte: dict,
    svi_konkretni_letovi: dict,
    svi_letovi,
    dan: date
) -> tuple:

    broj=0
    suma=0

    #prolazi test

    """for x in sve_karte.values():
        if x['datum_prodaje'] !=dan:
            continue
        else:
            broj+=1
            sifra= x['sifra_konkretnog_leta']
            konklet= svi_konkretni_letovi[sifra]
            broj_leta= konklet['broj_leta']
            let=svi_letovi[broj_leta]

            suma+= let['cena']"""

    #prolazi meni
    for x in sve_karte.values():
        x['datum_prodaje']=provera(x['datum_prodaje'])
        if x['datum_prodaje'].day!=dan.day or x['datum_prodaje'].month!=dan.month or x['datum_prodaje'].year!=dan.year:
            continue
        else:
            broj+=1
            sifra= x['sifra_konkretnog_leta']
            konklet= svi_konkretni_letovi[sifra]
            broj_leta= konklet['broj_leta']
            let=svi_letovi[broj_leta]

            suma+= let['cena']

    return broj,suma

"""
Funkcija kao rezultat vraća dve vrednosti: broj karata čiji je dan polaska leta na zadati dan i njihovu ukupnu cenu.
Rezultat se vraća kao torka. Npr. return broj, suma
"""
def izvestaj_ubc_prodatih_karata_za_dan_polaska(
    sve_karte: dict,
    svi_konkretni_letovi: dict,
    svi_letovi: dict,
    dan: date
) -> tuple:

    broj=0
    suma=0

    """for x in sve_karte.values():
        sifra=x['sifra_konkretnog_leta']
        if svi_konkretni_letovi[sifra]['datum_i_vreme_polaska'].day !=dan.day:
            continue
        else:
            broj+=1
            sifra= x['sifra_konkretnog_leta']
            konklet= svi_konkretni_letovi[sifra]
            broj_leta= konklet['broj_leta']
            let=svi_letovi[broj_leta]

            suma+= let['cena']"""

    for x in sve_karte.values():
        sifra=x['sifra_konkretnog_leta']
        if svi_konkretni_letovi[sifra]['datum_i_vreme_polaska'].day != dan.day or svi_konkretni_letovi[sifra]['datum_i_vreme_polaska'].month != dan.month or svi_konkretni_letovi[sifra]['datum_i_vreme_polaska'].year != dan.year:
            continue
        else:
            broj+=1
            sifra= x['sifra_konkretnog_leta']
            konklet= svi_konkretni_letovi[sifra]
            broj_leta= konklet['broj_leta']
            let=svi_letovi[broj_leta]

            suma+= let['cena']

    return broj, suma


"""
Funkcija kao rezultat vraća dve vrednosti: broj karata koje je zadati prodavac prodao na zadati dan i njihovu 
ukupnu cenu. Rezultat se vraća kao torka. Npr. return broj, suma
"""
def izvestaj_ubc_prodatih_karata_za_dan_prodaje_i_prodavca(
    sve_karte: dict,
    konkretni_letovi: dict,
    svi_letovi: dict,
    dan: date,
    prodavac: str
) -> tuple:

    broj=0
    suma=0
    # za testove
    """for x in sve_karte.values():
        if x['datum_prodaje']!= dan:
            continue
        elif x['prodavac']!= prodavac:
            continue
        else:
            broj+=1
            sifra= x['sifra_konkretnog_leta']
            konklet= konkretni_letovi[sifra]
            broj_leta= konklet['broj_leta']
            let=svi_letovi[broj_leta]

            suma+= let['cena']"""
    # za meni
    for x in sve_karte.values():
        x['datum_prodaje']=provera(x['datum_prodaje'])
        if not x.get('prodavac'):
            continue
        if isinstance(x['prodavac'], dict):
            if x['datum_prodaje'].day!=dan.day or x['datum_prodaje'].month!=dan.month or x['datum_prodaje'].year!=dan.year:
                continue
            elif x['prodavac'].get('korisnicko_ime')!= prodavac:
                continue
            else:
                broj+=1
                sifra= x['sifra_konkretnog_leta']
                konklet= konkretni_letovi[sifra]
                broj_leta= konklet['broj_leta']
                let=svi_letovi[broj_leta]

                suma+= let['cena']

    return broj,suma

"""
Funkcija kao rezultat vraća rečnik koji za ključ ima dan prodaje, a za vrednost broj karata prodatih na taj dan.
Npr: {"2023-01-01": 20}
"""
def izvestaj_ubc_prodatih_karata_30_dana_po_prodavcima(
    sve_karte: dict,
    svi_konkretni_letovi: dict,
    svi_letovi: dict
) -> dict: #ubc znaci ukupan broj i cena
    izvestaj={}
    
    danas= datetime.today()
    dan = danas - timedelta(days=30)
    prodavci= []
    for x in sve_karte.values():
        if x['prodavac'] not in prodavci and x['prodavac']!="":
            prodavci.append(x['prodavac'])

    for x in prodavci:
        broj=0
        suma=0

        for y in sve_karte.values():
            """datum =""
            if isinstance(y['datum_prodaje'],str):
                datum=datetime.strptime(y['datum_prodaje'], "%d.%m.%Y." )"""
            """
            elif isinstance(y['datum_prodaje'], datetime):
                datum= datetime.strftime(y['datum_prodaje'],"%d.%m.%Y.")
                datum= datetime.strptime(datum, "%d.%m.%Y.")"""
            
            #"%Y-%m-%d %H:%M:%S"
            try:
                if datetime.strptime(y['datum_prodaje'],"%Y-%m-%d %H:%M:%S.%f" )< dan:
                #if datum< dan:
                    continue
                elif  datetime.strptime(y['datum_prodaje'],"%Y-%m-%d %H:%M:%S.%f" )> danas :
                #elif  datum> danas :
                    continue

            except ValueError:
                if datetime.strptime(y['datum_prodaje'],"%d.%m.%Y." )< dan:
                #if datum< dan:
                    continue
                elif  datetime.strptime(y['datum_prodaje'],"%d.%m.%Y." )> danas :
                #elif  datum> danas :
                    continue
            
            if y['prodavac']!= x:
                continue
            else:
                broj+=1
                sifra= y['sifra_konkretnog_leta']
                konklet= svi_konkretni_letovi[sifra]
                broj_leta= konklet['broj_leta']
                let=svi_letovi[broj_leta]

                suma+= let['cena']
        try:
            t=(broj, suma, x)
            izvestaj[x]=t
        except TypeError:
            t=(broj, suma, x['korisnicko_ime'])
            izvestaj[x['korisnicko_ime']]=t

    return izvestaj

# {prodavac1: (brKarata1, ukupnaCena1, prodavac1), prodavac2: (brKarata2, ukupnaCena2, prodavac1)}

