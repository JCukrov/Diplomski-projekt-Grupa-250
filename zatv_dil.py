# 1 je kooperacija, 0 je izdaja
import random

from strategije import *
from vizualizacija import vizualiziraj_rezultate


def print_poredak(poredak, directory):
    with open(f'{directory}/poredak.csv', 'w+', encoding='UTF-8') as output:
        output.write(f'Rank;Ime;Bodovi\n')

        print("\n===== TABLICA PORETKA =====")
        for idx, ig in enumerate(poredak, start=1):
            print(f"{idx}. {ig.ime} - {ig.ukupni_bodovi} bodovi")
            output.write(f'{idx};{ig.ime};{ig.ukupni_bodovi}\n')


def igra(prvi, drugi, broj_igra, suppress_move_print = False) -> [int]:
    prosli1 = 1
    prosli2 = 1
    prvi.bodovi = 0
    drugi.bodovi = 0
    
    # Potezi: 1 oboje suradivali, 2 samo prvi igrac suradivao, 3  samo drugi igrac suradivao, 4 nitko nije suradivao  
    potezi = []

    for i in range(broj_igra):
        potez1 = prvi.igraj(i, prosli2)
        potez2 = drugi.igraj(i, prosli1)

        prosli1 = potez1
        prosli2 = potez2

        if(potez1 == 1 and potez2 == 1):
            potezi.append(1)
            prvi.bodovi = prvi.bodovi + 3
            drugi.bodovi = drugi.bodovi + 3
        elif(potez1 == 1 and potez2 == 0):
            potezi.append(2)
            drugi.bodovi = drugi.bodovi + 5
        elif(potez1 == 0 and potez2 == 1):
            potezi.append(3)
            prvi.bodovi = prvi.bodovi + 5
        else:
            potezi.append(4)
            prvi.bodovi = prvi.bodovi + 1
            drugi.bodovi = drugi.bodovi + 1

    if prvi.bodovi > drugi.bodovi:
        prvi.ukupni_bodovi += 3
    elif drugi.bodovi == prvi.bodovi:
        prvi.ukupni_bodovi += 1
        drugi.ukupni_bodovi += 1
    else: drugi.ukupni_bodovi +=3

    if not suppress_move_print:
        print("Igra zavrsena")
        print(f"Igrac {prvi.ime} osvojio je {prvi.bodovi} bodova")
        print(f"Igrac {drugi.ime} osvojio je {drugi.bodovi} bodova")
    return potezi



def zatv_dil(igraci, broj_igra = 200, directory = './output', suppress_move_print = False, suppress_visualization = False):

    protivnici = [type(i)() for i in igraci]
    
    sve_igre = []

    with open(f'{directory}/igre.csv', 'w+', encoding='UTF-8') as output:
        output.write('Prvi igrac;Bodovi Prvog;Drugi igrac;Bodovi drugog;Potezi\n')

        for i in range(len(igraci)):
            for j in range(i, len(protivnici)):
                potezi = igra(igraci[i], protivnici[j], broj_igra, suppress_move_print=suppress_move_print)
                
                # Spremi podatke za vizualizaciju
                sve_igre.append({
                    'prvi': igraci[i].ime,
                    'drugi': protivnici[j].ime,
                    'bodovi_prvi': igraci[i].bodovi,
                    'bodovi_drugi': protivnici[j].bodovi,
                    'potezi': potezi
                })
                
                output.write(f'{igraci[i].ime};{igraci[i].bodovi};{protivnici[j].ime};{protivnici[j].bodovi};{potezi}\n')

    poredak = sorted(igraci, key=lambda x: x.ukupni_bodovi, reverse=True)

    print_poredak(poredak = poredak, directory = directory)

    if not suppress_visualization:
        # Kreiraj vizualizacije
        print("\n===== KREIRANJE VIZUALIZACIJA =====")
        vizualiziraj_rezultate(poredak, sve_igre, directory)

    return poredak


if __name__ == "__main__":
    igraci = []
    igraci.append(TFT())
    igraci.append(TF2T())
    igraci.append(JOSS())
    igraci.append(FRIEDMAN())
    igraci.append(RANDOM())
    igraci.append(ADE())
    igraci.append(ACO())
    igraci.append(STFT())
    igraci.append(TTFT())
    igraci.append(WSLS())
    
    zatv_dil(igraci = igraci)