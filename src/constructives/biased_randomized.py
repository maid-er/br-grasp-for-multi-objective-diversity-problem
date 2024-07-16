'''Auxiliar functions to construct a Biased-Randomized solution'''
from structure.solution import Solution
import random
import math

from utils.logger import load_logger

logging = load_logger(__name__)

OBJECTIVE_FUNCTIONS = {0: 'MaxSum',
                       1: 'MaxMin'}


def construct(inst: dict, parameters: dict) -> Solution:
    '''The function constructs a solution for a given instance using a Biased Greedy Randomized
    Adaptive Search (B-GRASP) procedure with specified parameters.

    Args:
      inst (dict): a dictionary containing the instance data. The dictionary includes the number of
    nodes `n`, the number of nodes to be selected `p`, and a distance matrix `d` representing the
    distances from each node to the rest of the nodes.
    alpha
      parameters (dict): always contains a 'distibution' key that indicates the probability
    distribution that will be used to biase the node selection from the candidate list. If the
    distribution is geometric, it contains another 'beta' key with the its parameter, which
    determines the trade-off between exploration and exploitation in the construction of a solution.
    The closer 'beta' is from 0, the more uniform random will be the selection, thus, the
    construction will have a more exploratory behavior. If 'beta' is closer to 1, a greedier
    solution will be constructed.

    Returns:
        (Solution): contains the solution information..
    '''
    distribution = parameters.get('distribution')

    sol = Solution(inst)
    n = inst['n']
    u = random.randint(0, n-1)
    sol.add_to_solution(u)
    cl = create_candidate_list(sol, u)
    while not sol.satisfies_capacity():
        objective = len(cl) % 2  # 0: MaxSum, 1: MaxMin
        cl = [c for c in cl if sol.satisfies_cost([c[2]])]
        if len(cl) == 0:
            logging.error('No feasible solution reached in the construction phase.')
            sol = Solution(inst)
            sol.of_MaxMin = 0
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
        sol.add_to_solution(cSel[2], cSel[1], cSel[0])
        cl.remove(cSel)
        update_candidate_list(sol, cl, cSel[2])
    return sol


def create_candidate_list(sol: Solution, first: int) -> list:
    '''The function creates a list of candidate solutions based on the distance to the given
    solution and excluding the first candidate.

    Args:
      sol (Solution): contains the solution information.
      first (int): represents the ID of the first candidate element (node) in the solution. This
    index is used to exclude the first candidate from the candidate list that is being created.

    Returns:
      (list): a list of candidate solutions. Each candidate solution is represented as a list
    containing the sum of the distances to the rest of the nodes in the solution and the index
    of the candidate solution.
    '''
    n = sol.instance['n']
    cl = []
    for c in range(n):
        if c != first:
            d_sum = sol.distance_sum_to_solution(c)
            d_min = sol.minimum_distance_to_solution(c)
            cl.append([d_sum, d_min, c])
    return cl


def update_candidate_list(sol: Solution, cl: list, added: int):
    '''Iterates through a candidate list and updates the first element (sum of distances) of each
    candidate adding the distance to the new `added` element.

    Args:
      sol (Solution): contains the solution information.
      cl (list): a list of candidate solutions. Each candidate solution is represented as a list
    containing the sum of the distances and the minimum distance to the rest of the nodes in the
    solution, and the index of the candidate solution.
      added (int): represents the ID of the candidate that was added to the solution.
    '''
    for i in range(len(cl)):
        c = cl[i]
        c_to_added_distance = sol.instance['d'][added][c[2]]

        c[0] += c_to_added_distance
        if c_to_added_distance < c[1]:
            c[1] = c_to_added_distance
