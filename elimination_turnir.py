import copy
from pathlib import Path

from strategije import *
from turnir_utility import *
from zatv_dil import zatv_dil, print_poredak



def provedi_elimination_iter(igraci, path: Path, broj_igra: int = 200, suppress_move_print = False, suppress_visualization = False) -> list:
    '''
    Function conducts one iteration of an elimination tournament.
    Args:
        igraci - array of strategies
        path - path for data output
        broj_igra - number of games in a single round between two strategies
        suppress_move_print - if True disables each round point gain/loss
        suppress_visualization - if True prevents plotting of results
    Returns:
        list of strategies ordered by their performance (descending)
    '''

    counter: int = 1

    finalni_poredak = []

    while len(igraci) > 1:
        
        resetiraj_strategije(igraci, reset_cumul = True)
        Path(f'{path}/round_{counter}').mkdir(parents = True, exist_ok = True)
        
        print(f'======== {counter}. runda turnira =========')
        poredak = zatv_dil(igraci, broj_igra = broj_igra, directory = f'{path}/round_{counter}',
                            suppress_move_print = suppress_move_print, suppress_visualization = suppress_visualization)

        najgori = poredak[-1]

        finalni_poredak.insert(0, najgori)
        igraci.remove(najgori)
        
        counter += 1

    finalni_poredak.insert(0,igraci[0])

    with open(f'{path}/final_stats.csv', 'w') as output:
        output.write('Pozicija;Ime strategije\n')

        print("\n========= Finalni poredak turnira ===========")
        for idx, item in enumerate(finalni_poredak, start = 1):
            print(f'{idx}. {item.ime}')
            output.write(f'{idx};{item.ime}\n')

    return finalni_poredak


def single_elimination(path: str = './output/turnir') -> None:
    '''
    Function which sets up a tournament (used only when with one tournament instance). For more tournaments see: ponovi_natjecanja
    Args:
        path - path for data output 
    Returns:
        None
    '''

    # Izbrisi sve prethodne podatke iz turnira

    add_data_folder(path)

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
    igraci.append(DOWNING())
    igraci.append(FELD())
    igraci.append(SHUBIK())
    igraci.append(NYDEGGER())
    
    provedi_elimination_iter(igraci = igraci, path = path, broj_igra = 200)


def elimination(n: int = 100, path = './output/elimination_turnir') -> None:
    '''
    Function for conducting multiple tournaments and gathering data from them
    Args:
        n - number of tournaments to conduct
        path - path for data output
    Returns:
        None
    '''

    add_data_folder(path)
    
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
    igraci.append(DOWNING())
    igraci.append(FELD())
    igraci.append(SHUBIK())
    igraci.append(NYDEGGER())

    score = {}
    for item in igraci:
        score[item.ime] = 0
    for i in range(n):

        result = provedi_elimination_iter(path=f'{path}/turnir_{i+1}', igraci = copy.deepcopy(igraci), suppress_move_print = True, suppress_visualization = True)
        for rank, player in enumerate(reversed(result)):
            score[player.ime] += rank

    sorted_scores = sorted(score.items(), key = lambda x: x[1], reverse=True)


    with open(f'{path}/final_stats.csv', 'w') as output:

        output.write('Pozicija;Ime strategije;Broj bodova\n')

        print(f'\n\n=========== Poredak nakon {n} turnira ==========')
        for idx, (name, value) in enumerate(sorted_scores, start=1):
            print(f'{idx}. {name}: {value}')
            output.write(f'{idx};{name};{value}\n')


if __name__ == "__main__":
    elimination(1000)