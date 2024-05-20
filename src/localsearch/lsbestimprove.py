'''
Auxiliar function to apply Best Improve Local Search.
The worst selected element and best unselected element are interchanged to improve
the initial solution.
'''
from structure import solution

from utils.logger import load_logger

logging = load_logger(__name__)


def improve(sol: dict, maxIter: int = 50):
    '''Iteratively tries to improve a solution until no further improvements can be made.

    Args:
      sol (dict): contains the solution information in three key-value pairs: 'sol' with the set
    of selected candidates for the solution, 'of' with the objective value, and 'instance' that
    contains the instance data, with key 'd' representing the distance matrix between all the
    candidate nodes.
    '''
    count = 0
    abs_count = 0
    while count < maxIter and abs_count < maxIter*2:
        improve = try_improvement(sol)
        if not improve:
            count += 1
        abs_count += 1
    logging.info('Local search stopped with %s total IT and %s IT with no improvements.',
                 abs_count, count)


def try_improvement(sol: dict) -> bool:
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
     best_unselected, unsel_maxsum_variability, unsel_maxmin) = select_interchange(sol)

    if (sel_maxsum_variability <= unsel_maxsum_variability and sel_maxmin <= unsel_maxmin
        and solution.satisfies_cost(sol, best_unselected, worst_selected)
            and solution.satisfies_capacity(sol, best_unselected, worst_selected)):

        solution.add_to_solution(sol, best_unselected, unsel_maxmin, unsel_maxsum_variability)
        solution.remove_from_solution(sol, worst_selected, sel_maxsum_variability)
        return True
    return False


def select_interchange(sol: dict):
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
    for v in sol['sol']:
        d_sum = solution.distance_sum_to_solution(sol, v)
        d_min = solution.minimum_distance_to_solution(sol, v)
        if d_sum <= best_sum_sel and d_min <= best_min_sel:
            best_sum_sel = d_sum
            best_min_sel = d_min
            sel = v
    for v in range(n):
        if not solution.contains(sol, v):
            d_sum = solution.distance_sum_to_solution(sol, v, without=sel)
            d_min = solution.minimum_distance_to_solution(sol, v, without=sel)
            if d_sum >= best_sum_unsel and d_min >= best_min_unsel:
                best_sum_unsel = d_sum
                best_min_unsel = d_min
                unsel = v
    return sel, best_sum_sel, best_min_unsel, unsel, best_sum_unsel, best_min_unsel
