import copy
from pathlib import Path

from strategije import *
from zatv_dil import zatv_dil, print_poredak

def ask_yes_no(prompt: str = 'Yes or no?') -> bool:
    
    while True:
        answer = input(f'{prompt} [y/n]: ').strip().lower()
        if answer in ('y', 'yes'):
            return True
        elif answer in ('n', 'no'):
            return False
        print('Please enter y or n.')

def resetiraj_strategije(igraci):
   
    for item in igraci:
        item.__init__()
    return



def provedi_natjecanje(igraci, path: Path, broj_igra: int = 200, suppress_move_print = False, suppress_visualization = False):

    counter: int = 1

    finalni_poredak = []

    while len(igraci) > 1:

        Path(f'{path}/round_{counter}').mkdir(parents = True, exist_ok = True)
        
        print(f'======== {counter}. runda turnira =========')
        poredak = zatv_dil(igraci, broj_igra = broj_igra, directory = f'{path}/round_{counter}',
                            suppress_move_print = suppress_move_print, suppress_visualization = suppress_visualization)

        najgori = poredak[-1]

        finalni_poredak.insert(0, najgori)
        igraci.remove(najgori)

        resetiraj_strategije(igraci)
        
        counter += 1

    finalni_poredak.insert(0,igraci[0])

    with open(f'{path}/final_stats.csv', 'w') as output:
        output.write('Pozicija;Ime strategije\n')

        print("\n========= Finalni poredak turnira ===========")
        for idx, item in enumerate(finalni_poredak, start = 1):
            print(f'{idx}. {item.ime}')
            output.write(f'{idx};{item.ime}\n')

    return finalni_poredak


def natjecanje(path: str = './output/turnir', skip_confirm = False):

    # Izbrisi sve prethodne podatke iz turnira

    path = Path(f'{path}')

    if path.exists():
        if ask_yes_no("Pokretanjem ovog programa brišu se rezultati prethodnog turnira. Želite li nastaviti?"):
            path._delete()
        else:
            print('Prestanak rada.')
            exit(0)

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
    
    provedi_natjecanje(igraci = igraci, path = path, broj_igra = 200)


def ponovi_natjecanje(n: int = 100, path = './output/repeat_turnir'):

    path = Path(path)
    if path.exists():
        if ask_yes_no("Pokretanjem ovog programa brišu se rezultati prethodnih turnira. Želite li nastaviti?"):
            path._delete()
        else:
            print('Prestanak rada.')
            exit(0)
    
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

    score = {}
    for item in igraci:
        score[item.ime] = 0

    for i in range(n):

        result = provedi_natjecanje(path=f'{path}/turnir_{i+1}', igraci = copy.deepcopy(igraci), suppress_move_print = True, suppress_visualization = True)
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
    ponovi_natjecanje(100)