from pathlib import Path

def ask_yes_no(prompt: str = 'Yes or no?') -> bool:
    '''
    Prompts user a yes or no question
    Args:
        prompt - prompt for the user
    Returns:
        True - if user inputed y or yes
        False - if user inputed n or no
    '''
    
    while True:
        answer = input(f'{prompt} [y/n]: ').strip().lower()
        if answer in ('y', 'yes'):
            return True
        elif answer in ('n', 'no'):
            return False
        print('Please enter y or n.')

def resetiraj_strategije(igraci, reset_cumul = False) -> None:
    '''
    Function reinitializes strategies
    Args:
        igraci - list of strategies
    Returns:
        None
    '''
   
    for item in igraci:
        item.reset()
        if reset_cumul:
            item.kumulativni_bodovi = 0
    return


def add_data_folder(path: str):
    path = Path(path)
    if path.exists():
        if ask_yes_no("Pokretanjem ovog programa brišu se rezultati prethodnih turnira. Želite li nastaviti?"):
            path._delete()
        else:
            print('Prestanak rada.')
            exit(0)
    else:
        path.mkdir(parents = True, exist_ok = True)