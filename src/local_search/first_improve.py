'''
Auxiliar function to apply First Improve Local Search.
Objective functions selected and unselected elements are compared iteratively,
when the unselected element's result improves the selected one's, they are interchanged
in the solution.
'''
import datetime
from itertools import combinations

from constructives.biased_randomized import create_candidate_list
from structure.dominance import exchange_is_dominant
from structure.instance import get_all_pairwise_distances
from structure.solution import Solution

from utils.logger import load_logger

logging = load_logger(__name__)


def try_improvement(sol: Solution, objective: int, improvement_criteria: str,
                    switch: list = [1, 1], max_time: int = 5) -> bool:
    '''Attempts to improve a solution by selecting and interchanging a selected element (node)
    with an unselected element. The improvement is obtained if the new solution dominates the
    previous solution.

    Args:
      sol (Solution): contains the solution information.
      switch (list): indicates the neighborhood being analized in the local search. The first
    element defines how many nodes will be removed from the solution and the second element
    determines the number of nodes that will be added to the solution. Defaults to [1, 1] for
    a standard 1-1 exchange.
      max_time (int): maximum local search execution time in seconds. If no improvement is find
    in this time, the local search is stopped.

    Returns:
      (bool): `True` if the improvement was successful (i.e., if the objective values are
    dominant and constraints are met with the interchange), and `False` otherwise.
    '''
    selected, unselected = create_selected_unselected(sol, objective)
    # Select the first combination of size switch[0] in current solution and the first combination
    # of size switch[1] in unselected candidate list whose exchange makes a dominant new solution
    # that mets the constraints.
    selected_combinations = list(combinations(selected, switch[0]))
    unselected_combinations = list(combinations(unselected, switch[1]))

    start = datetime.datetime.now()
    for combo_s in selected_combinations:
        # If time is exceeded break LS without improvement
        if datetime.timedelta(seconds=max_time) < datetime.datetime.now() - start:
            print('Unable to find an improvement in the established time.')
            return False
        pairwise_d = get_all_pairwise_distances(sol.instance, combo_s)
        d_sum_s = [sol.distance_sum_to_solution(v) for v in combo_s] + pairwise_d
        d_min_s = [sol.minimum_distance_to_solution(v) for v in combo_s] + pairwise_d
        for combo_u in unselected_combinations:
            # If time is exceeded break LS without improvement
            if datetime.timedelta(seconds=max_time) < datetime.datetime.now() - start:
                print('Unable to find an improvement in the established time.')
                return False
            pairwise_d = get_all_pairwise_distances(sol.instance, combo_u)
            d_sum_u = [sol.distance_sum_to_solution(v, without=combo_s)
                       for v in combo_u] + pairwise_d
            d_min_u = [sol.minimum_distance_to_solution(v, without=combo_s)
                       for v in combo_u] + pairwise_d

            # TODO IMPROVE CODE
            # Check if new solution improves the latest depending on the selected criteria
            if improvement_criteria == 'Dom':
                new_improves_old = exchange_is_dominant(sum(d_sum_s), min(d_min_s),
                                                        sum(d_sum_u), min(d_min_u))
            else:
                if objective == 0:
                    new_improves_old = sum(d_sum_s) < sum(d_sum_u)
                else:
                    new_improves_old = min(d_min_s) < min(d_min_u)

            if new_improves_old \
                and sol.satisfies_cost(combo_u, combo_s) \
                    and sol.satisfies_capacity(combo_u, combo_s):

                for v in combo_u:
                    sol.add_to_solution(v, min(d_min_u), sum(d_sum_u))
                for u in combo_s:
                    sol.remove_from_solution(u, min(d_min_s), sum(d_sum_s))

                return True
    return False


def create_selected_unselected(sol: Solution, objective: int):
    '''Takes a solution instance as input and returns two lists - one containing selected items
    and the other containing unselected items based on the solution. The selected elements are
    sorted in reverse order according to the objective function. Meanwhile, the unselected
    elements are sorted from the best candidate to the worst.

    Args:
      sol (Solution): contains the solution information.

    Returns:
      selected (list): contains the candidates selected in the current solution.
      unselected (list): contains the unselected candidates in the current solution.
    '''
    cl = create_candidate_list(sol)

    selected = []
    unselected = []

    for v in cl:
        if sol.contains(v[2]):
            selected.append(v)
        else:
            unselected.append(v)

    selected.sort(key=lambda row: row[objective])  # Sort from worst to best
    unselected.sort(key=lambda row: -row[objective])  # Sort from best to worst
    # Get only the node ID
    selected = [s[2] for s in selected]
    unselected = [u[2] for u in unselected]

    return selected, unselected
