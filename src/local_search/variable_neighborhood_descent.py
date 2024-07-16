'''
Auxiliar function to apply Variable Neighborhood Descent with Best Improve Local Search.
The worst selected element and best unselected element are interchanged to improve
the initial solution.
'''
from local_search import best_improve as bs
from local_search import first_improve as fs
from structure.solution import Solution

from utils.logger import load_logger

logging = load_logger(__name__)


def improve(sol: Solution, config: dict):
    '''Iteratively tries to improve a solution until no further improvements can be made.

    Args:
      sol (Solution): contains the solution information.
    '''
    ls_scheme = config.get('scheme')
    neighborhoods = {1: [1, 1],
                     2: [1, 2],
                     3: [2, 1]}

    nb = 1
    count = 0
    abs_count = 0
    improve = True
    while improve or nb <= len(neighborhoods):
        switch = neighborhoods[nb]
        logging.info('Local searching in neighbourhood %s with switch type %s.', nb, switch)
        if ls_scheme == 'Best':
            improve = bs.try_improvement(sol, switch)
        elif ls_scheme == 'First':
            improve = fs.try_improvement(sol, switch)
        if improve:
            logging.info('Improved solution.')
            nb = 1
        else:
            logging.info('Unable to improve solution. Change neighborhood.')
            count += 1
            nb += 1
        abs_count += 1
    logging.info('Local search stopped with %s total IT and %s IT with no improvements.',
                 abs_count, count)
