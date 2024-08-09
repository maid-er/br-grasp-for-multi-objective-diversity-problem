'''
Auxiliar function to apply First Improve Local Search.
Objective functions of ramdomly sorted selected and unselected elements are compared,
when the unselected element's result improves the selected one's, they are interchanged
in the solution.
'''
import random
from itertools import combinations

from structure.dominance import exchange_is_dominant
from structure.instance import get_all_pairwise_distances
from structure.solution import Solution


def improve(sol: Solution):
    '''Iteratively tries to improve a solution until no further improvements can be made.

    Args:
      sol (Solution): contains the solution information.
    '''
    improve = True
    while improve:
        improve = try_improvement(sol)


def try_improvement(sol: Solution, switch: list = [1, 1]) -> bool:
    '''Attempts to improve a solution by selecting and interchanging a selected element (node)
    with an unselected element. The improvement is obtained if the new solution dominates the
    previous solution.

    Args:
      sol (Solution): contains the solution information.
      switch (list): indicates the neighborhood being analized in the local search. The first
    element defines how many nodes will be removed from the solution and the second element
    determines the number of nodes that will be added to the solution. Defaults to [1, 1] for
    a standard 1-1 exchange.

    Returns:
      (bool): `True` if the improvement was successful (i.e., if the objective values are
    dominant and constraints are met with the interchange), and `False` otherwise.
    '''
    selected, unselected = create_selected_unselected(sol)
    random.shuffle(selected)
    random.shuffle(unselected)
    # Select the first combination of size switch[0] in current solution and the first combination
    # of size switch[1] in unselected candidate list whose exchange makes a dominant new solution
    # that mets the constraints.
    for combo_s in combinations(selected, switch[0]):
        pairwise_d = get_all_pairwise_distances(sol.instance, combo_s)
        d_sum_s = [sol.distance_sum_to_solution(v) for v in combo_s] + pairwise_d
        d_min_s = [sol.minimum_distance_to_solution(v) for v in combo_s] + pairwise_d
        for combo_u in combinations(unselected, switch[1]):
            pairwise_d = get_all_pairwise_distances(sol.instance, combo_u)
            d_sum_u = [sol.distance_sum_to_solution(v, without=combo_s)
                       for v in combo_u] + pairwise_d
            d_min_u = [sol.minimum_distance_to_solution(v, without=combo_s)
                       for v in combo_u] + pairwise_d

            new_dominates_old = exchange_is_dominant(sum(d_sum_s), min(d_min_s),
                                                     sum(d_sum_u), min(d_min_u))

            if new_dominates_old \
                and sol.satisfies_cost(combo_u, combo_s) \
                    and sol.satisfies_capacity(combo_u, combo_s):

                for v in combo_u:
                    sol.add_to_solution(v, min(d_min_u), sum(d_sum_u))
                for u in combo_s:
                    sol.remove_from_solution(u, min(d_min_s), sum(d_sum_s))

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
