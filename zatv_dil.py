# 1 je kooperacija, 0 je izdaja
import random

from strategije import *
from vizualizacija import vizualiziraj_rezultate


def print_poredak(poredak, directory) -> None:
    '''
    Prints the final ranking to the stdout and file
    Args:
        poredak - orderd ranking of strategies (desc)
        directory - directory where to output the results
    Returns:
        None
    '''
    with open(f'{directory}/poredak.csv', 'w+', encoding='UTF-8') as output:
        output.write(f'Rank;Ime;Bodovi\n')

        print("\n===== TABLICA PORETKA =====")
        for idx, ig in enumerate(poredak, start=1):
            print(f"{idx}. {ig.ime} - {ig.kumulativni_bodovi} bodovi")
            output.write(f'{idx};{ig.ime};{ig.kumulativni_bodovi}\n')


def igra(prvi, drugi, broj_igra: int, suppress_move_print: bool = False) -> [int]:
    '''
    Conducts one game between two strategies
    Args:
        prvi - first strategy
        drugi - second strategy
        broj_igra - number of games in a single round between two strategies
        directory - directory where to output the results
        suppress_move_print - if True disables each round point gain/loss
    Returns:
        array of all moves made each round (1. - both cooperated, 2. - only the first player cooperated, 3. only the second player cooperated, 4. neither player cooperated)
    '''

    prosli1 = 1
    prosli2 = 1

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

    prvi.kumulativni_bodovi += prvi.bodovi
    drugi.kumulativni_bodovi += drugi.bodovi

    if prvi.bodovi > drugi.bodovi:
        prvi.ukupni_bodovi += 3
    elif prvi.bodovi == drugi.bodovi:
        prvi.ukupni_bodovi += 1
        drugi.ukupni_bodovi += 1
    else: drugi.ukupni_bodovi +=3

    if not suppress_move_print:
        print("Igra zavrsena")
        print(f"Igrac {prvi.ime} osvojio je {prvi.bodovi} bodova")
        print(f"Igrac {drugi.ime} osvojio je {drugi.bodovi} bodova")
    return potezi



def zatv_dil(igraci, broj_igra: int = 200, directory = './output', suppress_move_print: bool = False, suppress_visualization: bool = False):
    '''
    Conducts one game of the Prisoners Dilemma between each of the strategies
    Args:
        igraci - array of strategies
        broj_igra - number of games in a single round between two strategies
        directory - directory where to output the results
        suppress_move_print - if True disables each round point gain/loss
        suppress_visualization - if True prevents plotting of results
    Returns:
        ordered array of strategies based on performance (descending)
    '''
    
    sve_igre = []

    with open(f'{directory}/igre.csv', 'w+', encoding='UTF-8') as output:
        output.write('Prvi igrac;Bodovi Prvog;Drugi igrac;Bodovi drugog;Potezi\n')

        for i in range(len(igraci)):
            for j in range(i+1, len(igraci)):
                
                # resetiraj atribute i bodove strategija
                igraci[i].reset()
                igraci[j].reset()

                potezi = igra(igraci[i], igraci[j], broj_igra, suppress_move_print=suppress_move_print)
                
                # Spremi podatke za vizualizaciju
                sve_igre.append({
                    'prvi': igraci[i].ime,
                    'drugi': igraci[j].ime,
                    'bodovi_prvi': igraci[i].bodovi,
                    'bodovi_drugi': igraci[j].bodovi,
                    'potezi': potezi
                })
                
                output.write(f'{igraci[i].ime};{igraci[i].bodovi};{igraci[j].ime};{igraci[j].bodovi};{potezi}\n')

    poredak = sorted(igraci, key=lambda x: x.kumulativni_bodovi, reverse=True)

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