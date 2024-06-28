'''
Auxiliar function to apply First Improve Local Search.
Objective functions of ramdomly sorted selected and unselected elements are compared,
when the unselected element's result improves the selected one's, they are interchanged
in the solution.
'''
import random

from structure.solution import Solution


def improve(sol: Solution):
    '''Iteratively tries to improve a solution until no further improvements can be made.

    Args:
      sol (Solution): contains the solution information.
    '''
    improve = True
    while improve:
        improve = try_improvement(sol)


def try_improvement(sol: Solution) -> bool:
    '''Attempts to improve a solution by selecting and interchanging a selected element (node)
    with an unselected element. The improvement is obtained if the sum of the distances of the
    new element to the rest of the selected nodes is higher than the distance of the previous
    selection.

    Args:
      sol (Solution): contains the solution information.

    Returns:
      (bool): `True` if the improvement was successful (i.e., if the objective values are
    improved and constraints are met with the interchange), and `False` otherwise.
    '''
    selected, unselected = create_selected_unselected(sol)
    random.shuffle(selected)
    random.shuffle(unselected)
    for s in selected:
        d_sum_s = sol.distance_sum_to_solution(s)
        d_min_s = sol.minimum_distance_to_solution(s)
        for u in unselected:
            d_sum_u = sol.distance_sum_to_solution(u, s)
            d_min_u = sol.minimum_distance_to_solution(u, s)
            if d_sum_u > d_sum_s and d_min_u > d_min_s:
                sol.remove_from_solution(s, d_min_s, d_sum_s)
                sol.add_to_solution(u, d_min_u, d_sum_u)
                return True
    return False


def create_selected_unselected(sol: Solution):
    '''Takes a solution instance as input and returns two lists - one containing selected items
    and the other containing unselected items based on the solution.

    Args:
      sol (Solution): contains the solution information.

    Returns:
      selected (list): contains the candidates selected in the current solution.
      unselected (list): contains the unselected candidates in the current solution.
    '''
    selected = []
    unselected = []
    n = sol.instance['n']
    for v in range(n):
        if sol.contains(v):
            selected.append(v)
        else:
            unselected.append(v)
    return selected, unselected
