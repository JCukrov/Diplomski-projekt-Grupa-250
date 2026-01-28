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

def natjecanje(broj_igra: int = 200):

    # Izbrisi sve prethodne podatke iz turnira

    path = Path(f'./output/turnir')

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
    igraci.append(DOWNING())
    igraci.append(FELD())
    igraci.append(SHUBIK())
    igraci.append(NYDEGGER())

    counter: int = 1

    finalni_poredak = []

    while len(igraci) > 1:

        Path(f'{path}/round_{counter}').mkdir(parents = True, exist_ok = True)
        
        print(f'======== {counter}. runda turnira =========')
        poredak = zatv_dil(igraci, broj_igra = broj_igra, directory = f'{path}/round_{counter}')

        najgori = poredak[-1]

        finalni_poredak.insert(0, najgori)
        igraci.remove(najgori)

        resetiraj_strategije(igraci)
        
        counter += 1

    finalni_poredak.insert(0,igraci[0])

    print("========= Finalni poredak turnira ===========")
    for idx, item in enumerate(finalni_poredak, start = 1):
        print(f'{idx}. {item.ime}')

if __name__ == "__main__":
    natjecanje()