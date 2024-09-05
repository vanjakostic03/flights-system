

import csv

"""
Funkcija kreira rečnik za novi aerodrom i dodaje ga u rečnik svih aerodroma.
Kao rezultat vraća rečnik svih aerodroma sa novim aerodromom.
"""
def kreiranje_aerodroma(
    svi_aerodromi: dict,
    skracenica: str ="",
    pun_naziv: str ="",
    grad: str ="",
    drzava: str =""
) -> dict:
    if skracenica == "":
        raise Exception('greska')

    if pun_naziv == "":
        raise Exception('greska')

    if grad == "":
        raise Exception('greska')

    if drzava == "":
        raise Exception('greska')

    aerodrom={
        'skracenica' : skracenica,
        'pun_naziv' : pun_naziv,
        'grad' : grad,
        'drzava' : drzava
    }

    svi_aerodromi[skracenica]=aerodrom

    return svi_aerodromi

"""
Funkcija koja čuva aerodrome u fajl.
"""
def sacuvaj_aerodrome(putanja: str, separator: str, svi_aerodromi: dict):
    with open(putanja, mode='w') as csv_file:
        polja=['skracenica','pun_naziv','grad','drzava']
        writer= csv.DictWriter(csv_file,fieldnames=polja, delimiter=separator)

        writer.writeheader()
        writer.writerows(svi_aerodromi.values())

"""
Funkcija koja učitava aerodrome iz fajla.
"""
def ucitaj_aerodrom(putanja: str, separator: str) -> dict:
    dict1={ }
    with open(putanja, mode='r') as csv_file:
        csvreader = csv.DictReader(csv_file,delimiter= separator)
        for row in csvreader :
            dict1[row['skracenica']] ={'skracenica': row['skracenica'], 'pun_naziv':row['pun_naziv'],'grad': row['grad'], 'drzava':row['drzava']}


    return dict1