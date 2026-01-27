import copy
from pathlib import Path

from strategije import *
from turnir_utility import *
from zatv_dil import zatv_dil



def round_robin(n: int = 100, path: str = './output/round_robin'):
    '''
    Conducts a repeated tournament and assigns points based on tournament performance. Points are scored according to their ranking: last place gets 0 points, second-to-last gets 1 and so on
    Args:
        n - number of tournaments
        path - output folder for data
    Returns:
        None
    '''

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

    add_data_folder(path)

    for i in range(n):

        # Resetiraj stanja strategija
        resetiraj_strategije(igraci)
        Path(f'{path}/turnir_{i+1}').mkdir(parents = True, exist_ok = True)

        result = zatv_dil(igraci=copy.deepcopy(igraci), directory=f'{path}/turnir_{i+1}', suppress_move_print=True, suppress_visualization=True)

        for rank, player in enumerate(reversed(result)):
            score[player.ime] += rank

    sorted_result = sorted(score.items(), key = lambda x: x[1], reverse=True)

    with open(f'{path}/final_stats.csv', 'w') as output:
        output.write('Pozicija;Ime strategije;Broj bodova\n')

        print(f'\n\n========== Poredak nakon {n} turnira ==========')

        for idx, (name, points) in enumerate(sorted_result, start=1):
            print(f'{idx}. {name}: {points}')
            output.write(f'{idx};{name};{points}')

if __name__ == '__main__':
    round_robin(1000)