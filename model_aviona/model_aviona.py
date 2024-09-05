import csv

import ast
"""
Funkcija kreira novi rečnik za model aviona i dodaje ga u rečnik svih modela aviona.
Kao rezultat vraća rečnik svih modela aviona sa novim modelom.
"""
id = 0


def kreiranje_modela_aviona(
    svi_modeli_aviona: dict,
    naziv: str ="",
    broj_redova: str = "",
    pozicije_sedista: list = []
) -> dict:

    global id

    if naziv == "" or naziv is None:
        raise Exception('greska')
    
    if broj_redova == "" or broj_redova is None:
        raise Exception('greska')

    if len(pozicije_sedista)==0 or pozicije_sedista is None:
        raise Exception('greska')

    model={
        'id': id,
        'naziv' : naziv,
        'broj_redova' : broj_redova,
        'pozicije_sedista' : pozicije_sedista
    }
    svi_modeli_aviona[id]=model
    id+=1
    return svi_modeli_aviona


"""
Funkcija čuva sve modele aviona u fajl na zadatoj putanji sa zadatim operatorom.
"""
def sacuvaj_modele_aviona(putanja: str, separator: str, svi_aerodromi: dict):
    with open(putanja, mode='a') as csv_file:
        polja=['id','naziv','broj_redova','pozicije_sedista']
        writer= csv.DictWriter(csv_file,fieldnames=polja, delimiter=separator)

        writer.writeheader()
        writer.writerows(svi_aerodromi.values())


"""
Funkcija učitava sve modele aviona iz fajla na zadatoj putanji sa zadatim operatorom.
"""
def ucitaj_modele_aviona(putanja: str, separator: str) -> dict:
    dict1={ }
    with open(putanja, mode='r') as csv_file:
        csvreader = csv.DictReader(csv_file,delimiter= separator)
        for row in csvreader :
            dict1[int(row['id'])] ={'id': int(row['id']),'naziv':row['naziv'], 'broj_redova':ast.literal_eval(row['broj_redova']),'pozicije_sedista': ast.literal_eval(row['pozicije_sedista'])}


    return dict1
