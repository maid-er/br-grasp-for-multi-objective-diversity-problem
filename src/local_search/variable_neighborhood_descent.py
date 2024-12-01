'''
Auxiliar function to apply Variable Neighborhood Descent.
'''
from local_search import best_improve as bes
from local_search import fast_improve as fas
from local_search import first_improve as fis
from structure.solution import Solution

from utils.logger import load_logger

logging = load_logger(__name__)

OBJECTIVE_FUNCTIONS = {0: 'MaxSum',
                       1: 'MaxMin'}


def improve(sol: Solution, config: dict):
    '''Iteratively tries to improve a solution until no further improvements can be made.

    Args:
      sol (Solution): contains the solution information.
    '''
    ls_scheme = config.get('scheme')
    if config.get('strategy') == 'VND':
        neighborhoods = config.get('neighborhoods')
    else:
        neighborhoods = {1: [1, 1]}

    max_time = config.get('execution_limits').get('max_local_search_time')
    max_it = config.get('execution_limits').get('max_local_search_it')

    nb = 1
    count = 0
    abs_count = 0
    improve = True
    while (improve or nb <= len(neighborhoods)) and abs_count < max_it:
        objective = abs_count % 2  # 0: MaxSum, 1: MaxMin (for Alt approach)
        # Check if a single objective approach is selected
        mo_approach = config.get('mo_approach_LS')
        if mo_approach == 'MaxSum':
            objective = 0
        elif mo_approach == 'MaxMin':
            objective = 1

        switch = neighborhoods[nb]
        print('Local searching in neighbourhood %s with switch type %s and %s objective.',
              nb, switch, 'Dom' if mo_approach == 'Dom' else OBJECTIVE_FUNCTIONS.get(objective))
        if ls_scheme == 'Best':
            improve = bes.try_improvement(sol, switch=switch, max_time=max_time)
        elif ls_scheme == 'Fast':
            improve = fas.try_improvement(sol, switch)
        elif ls_scheme == 'First':
            improve = fis.try_improvement(sol, objective, mo_approach, switch)
        if improve:
            print('Improved solution.')
            nb = 1
        else:
            print('Unable to improve solution. Change neighborhood.')
            count += 1
            nb += 1
        abs_count += 1
    print('Local search stopped with %s total IT and %s IT with no improvements.',
          abs_count, count)
