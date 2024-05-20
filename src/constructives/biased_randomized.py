'''Auxiliar functions to construct a Biased-Randomized solution'''
from structure import solution
import random
import math

from utils.logger import load_logger

logging = load_logger(__name__)

OBJECTIVE_FUNCTIONS = {0: 'MaxSum',
                       1: 'MaxMin'}


def construct(inst: dict, parameters: dict) -> dict:
    '''The function constructs a solution for a given instance using a Greedy Randomized Adaptive
    Search (GRASP) procedure with a specified alpha parameter.

    Args:
      inst (dict): a dictionary containing the instance data. The dictionary includes the number of
    nodes `n`, the number of nodes to be selected `p`, and a distance matrix `d` representing the
    distances from each node to the rest of the nodes.
    alpha
      alpha (float): a value that determines the trade-off between exploration and exploitation in
    the construction of a solution. It is used to calculate a threshold value `th`. This value is
    used to restrict the candidate list from which the element to be added to the solution is
    selected.

    Returns:
        (dict): contains the solution information in three key-value pairs: 'sol' with the set
    of selected candidates for the solution, 'of' with the objective value, and 'instance' that
    contains the instance data, with key 'd' representing the distance matrix between all the
    candidate nodes.
    '''
    distribution = parameters.get('distribution')

    sol = solution.create_empty_solution(inst)
    n = inst['n']
    u = random.randint(0, n-1)
    solution.add_to_solution(sol, u)
    cl = create_candidate_list(sol, u)
    while not solution.satisfies_capacity(sol):
        objective = len(cl) % 2  # 0: MaxSum, 1: MaxMin
        cl = [c for c in cl if solution.satisfies_cost(sol, c[2])]
        if len(cl) == 0:
            logging.error('No feasible solution reached in the construction phase.')
            break
        cl.sort(key=lambda row: -row[objective])
        logging.info('Sorted biased candidate list with %s objective.',
                     OBJECTIVE_FUNCTIONS.get(objective))

        if distribution == 'Geometric':
            beta = parameters.get('beta')
            beta = beta if beta >= 0 else random.random()
            selIdx = int(math.log(random.random()) / math.log(1 - beta))
            selIdx = selIdx % len(cl)
        elif distribution == 'Triangular':
            selIdx = int(len(cl) * (1 - math.sqrt(random.random())))

        cSel = cl[selIdx]
        solution.add_to_solution(sol, cSel[2], cSel[1], cSel[0])
        cl.remove(cSel)
        update_candidate_list(sol, cl, cSel[2])
    return sol


def create_candidate_list(sol: dict, first: int):
    '''The function creates a list of candidate solutions based on the distance to the given
    solution and excluding the first candidate.

    Args:
      sol (dict): contains the solution information in three key-value pairs: 'sol' with the set
    of selected candidates for the solution, 'of' with the objective value, and 'instance' that
    contains the instance data, with key 'd' representing the distance matrix between all the
    candidate nodes.
      first (int): represents the ID of the first candidate element (node) in the solution. This
    index is used to exclude the first candidate from the candidate list that is being created.

    Returns:
      (list): a list of candidate solutions. Each candidate solution is represented as a list
    containing the sum of the distances to the rest of the nodes in the solution and the index
    of the candidate solution.
    '''
    n = sol['instance']['n']
    cl = []
    for c in range(n):
        if c != first:
            d_sum = solution.distance_sum_to_solution(sol, c)
            d_min = solution.minimum_distance_to_solution(sol, c)
            cl.append([d_sum, d_min, c])
    return cl


def update_candidate_list(sol: dict, cl: list, added: int):
    '''Iterates through a candidate list and updates the first element (sum of distances) of each
    candidate adding the distance to the new `added` element.

    Args:
      sol (dict): contains the solution information in three key-value pairs: 'sol' with the set
    of selected candidates for the solution, 'of' with the objective value, and 'instance' that
    contains the instance data, with key 'd' representing the distance matrix between all the
    candidate nodes.
      cl (list): a list of candidate solutions. Each candidate solution is represented as a list
    containing the sum of the distances to the rest of the nodes in the solution and the index
    of the candidate solution.
      added (int): represents the ID of the candidate that was added to the solution.
    '''
    for i in range(len(cl)):
        c = cl[i]
        c_to_added_distance = sol['instance']['d'][added][c[2]]

        c[0] += c_to_added_distance
        if c_to_added_distance < c[1]:
            c[1] = c_to_added_distance
