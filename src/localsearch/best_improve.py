'''
Auxiliar function to apply Best Improve Local Search.
The worst selected element and best unselected element are interchanged to improve
the initial solution.
'''
from itertools import combinations

from structure.solution import Solution
from utils.logger import load_logger

logging = load_logger(__name__)


def improve(sol: Solution, max_iter: int = 50):
    '''Iteratively tries to improve a solution until no further improvements can be made.

    Args:
      sol (Solution): contains the solution information.
      max_iter (int): maximum number of iterations with no improvements.
    '''
    count = 0
    abs_count = 0
    while count < max_iter and abs_count < max_iter*2:
        improve = try_improvement(sol)
        if not improve:
            count += 1
        abs_count += 1
    logging.info('Local search stopped with %s total IT and %s IT with no improvements.',
                 abs_count, count)


def try_improvement(sol: Solution, neighborhood: int = [1, 1]) -> bool:
    '''Attempts to improve a solution by selecting and interchanging a selected element (node)
    with an unselected element. The improvement is obtained if the sum of the distances of the
    new element to the rest of the selected nodes is higher than the distance of the previous
    selection.

    Args:
        sol (Solution): contains the solution information.

    Returns:
    (bool): `True` if the improvement was successful (i.e., if `ofVarSel` is less than
    `ofVarUnsel`), and `False` otherwise.
    '''
    (worst_selected,
     sel_maxsum_variability, sel_maxmin,
     best_unselected,
     unsel_maxsum_variability, unsel_maxmin) = select_interchange(sol, neighborhood)

    if (sel_maxsum_variability <= unsel_maxsum_variability) and (sel_maxmin <= unsel_maxmin):

        for v in best_unselected:
            sol.add_to_solution(v, unsel_maxmin, unsel_maxsum_variability)
        for u in worst_selected:
            sol.remove_from_solution(u, sel_maxmin, sel_maxsum_variability)
        return True
    return False


def select_interchange(sol: Solution, neighborhood: list):
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
    n = sol.instance['n']
    sel = -1
    best_sum_sel = 0x3f3f3f3f
    best_min_sel = 0x3f3f3f3f
    unsel = -1
    best_sum_unsel = 0
    best_min_unsel = 0
    for combo in combinations(sol.solution_set, neighborhood[0]):
        d_sum = [sol.distance_sum_to_solution(v) for v in combo]
        d_min = [sol.minimum_distance_to_solution(v) for v in combo]
        if sum(d_sum) <= best_sum_sel and max(d_min) <= best_min_sel:
            best_sum_sel = sum(d_sum)
            best_min_sel = max(d_min)
            sel = list(combo)

    for combo in combinations(range(n), neighborhood[1]):
        if not any(sol.contains(v) for v in combo):
            d_sum = [sol.distance_sum_to_solution(v, without=sel) for v in combo]
            d_min = [sol.minimum_distance_to_solution(v, without=sel) for v in combo]
            if sum(d_sum) >= best_sum_unsel and max(d_min) >= best_min_unsel \
                and sol.satisfies_cost(combo, sel) \
                    and sol.satisfies_capacity(combo, sel):

                best_sum_unsel = sum(d_sum)
                best_min_unsel = max(d_min)
                unsel = list(combo)

    return sel, best_sum_sel, best_min_sel, unsel, best_sum_unsel, best_min_unsel
