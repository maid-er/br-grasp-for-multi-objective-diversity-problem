'''
Auxiliar function to apply Variable Neighborhood Descent with Best Improve Local Search.
The worst selected element and best unselected element are interchanged to improve
the initial solution.
'''
from itertools import combinations

from structure import solution

from utils.logger import load_logger

logging = load_logger(__name__)


def improve(sol: dict, max_iter: int = 50):
    '''Iteratively tries to improve a solution until no further improvements can be made.

    Args:
      sol (dict): contains the solution information in three key-value pairs: 'sol' with the set
    of selected candidates for the solution, 'of' with the objective value, and 'instance' that
    contains the instance data, with key 'd' representing the distance matrix between all the
    candidate nodes.
    '''
    neighborhoods = {1: [1, 1],
                     2: [1, 2],
                     3: [2, 1]}

    nb = 1
    count = 0
    abs_count = 0
    while count < max_iter and abs_count < max_iter*2:
        switch = neighborhoods[nb]
        logging.info('Local searching in neighbourhood %s with switch type %s.', nb, switch)
        improve = try_improvement(sol, switch)
        if not improve:
            logging.info('Unable to improve solution. Change neighborhood.')
            count += 1
            if nb < 3:
                nb += 1
            else:
                break
        else:
            logging.info('Improved solution.')
            nb = 1
        abs_count += 1
    logging.info('Local search stopped with %s total IT and %s IT with no improvements.',
                 abs_count, count)


def try_improvement(sol: dict, neighborhood) -> bool:
    '''Attempts to improve a solution by selecting and interchanging a selected element (node)
    with an unselected element. The improvement is obtained if the sum of the distances of the
    new element to the rest of the selected nodes is higher than the distance of the previous
    selection.

    Args:
      sol (dict): contains the solution information in three key-value pairs: 'sol' with the set
    of selected candidates for the solution, 'of' with the objective value, and 'instance' that
    contains the instance data, with key 'd' representing the distance matrix between all the
    candidate nodes.

    Returns:
      (bool): `True` if the improvement was successful (i.e., if `ofVarSel` is less than
    `ofVarUnsel`), and `False` otherwise.
    '''
    (worst_selected, sel_maxsum_variability, sel_maxmin,
     best_unselected, unsel_maxsum_variability, unsel_maxmin) = select_interchange(sol, neighborhood)

    if (sel_maxsum_variability <= unsel_maxsum_variability) and (sel_maxmin <= unsel_maxmin):

        for v in best_unselected:
            solution.add_to_solution(sol, v, unsel_maxmin, unsel_maxsum_variability)
        for u in worst_selected:
            solution.remove_from_solution(sol, u, sel_maxsum_variability)
        return True
    return False


def select_interchange(sol: dict, neighborhood: list):
    '''Interchanges the worst element in solution (lowest sum of distances to the rest of the
    selected elements) with the best unselected element (highest sum of distances to the rest
    of the selected elements).

    Args:
      sol (dict): contains the solution information in three key-value pairs: 'sol' with the set
    of selected candidates for the solution, 'of' with the objective value, and 'instance' that
    contains the instance data, with key 'd' representing the distance matrix between all the
    candidate nodes.

    Returns:
      sel (int): worst selected element ID.
      bestSel (float): sum of distances from `sel` to the rest of the elements in solution.
      unsel (int): best unselected element ID.
      bestUnsel (float): sum of distances from `unsel` to the rest of the elements in solution.
    '''
    n = sol['instance']['n']
    sel = -1
    best_sum_sel = 0x3f3f3f3f
    best_min_sel = 0x3f3f3f3f
    unsel = -1
    best_sum_unsel = 0
    best_min_unsel = 0
    for combo in combinations(sol['sol'], neighborhood[0]):
        d_sum = [solution.distance_sum_to_solution(sol, v) for v in combo]
        d_min = [solution.minimum_distance_to_solution(sol, v) for v in combo]
        if sum(d_sum) <= best_sum_sel and min(d_min) <= best_min_sel:
            best_sum_sel = sum(d_sum)
            best_min_sel = min(d_min)
            sel = list(combo)

    for combo in combinations(range(n), neighborhood[1]):
        if not any(solution.contains(sol, v) for v in combo):
            d_sum = [solution.distance_sum_to_solution(sol, v, without=sel) for v in combo]
            d_min = [solution.minimum_distance_to_solution(sol, v, without=sel) for v in combo]
            if sum(d_sum) >= best_sum_unsel and min(d_min) >= best_min_unsel \
                and solution.satisfies_cost(sol, combo, sel) \
                    and solution.satisfies_capacity(sol, combo, sel):

                best_sum_unsel = sum(d_sum)
                best_min_unsel = min(d_min)
                unsel = list(combo)

    return sel, best_sum_sel, best_min_sel, unsel, best_sum_unsel, best_min_unsel
