'''Auxiliar functions to construct a greedy solution'''
from structure import solution
import random


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
    alpha = parameters.get('alpha')

    sol = solution.create_empty_solution(inst)
    n = inst['n']
    u = random.randint(0, n-1)
    solution.add_to_solution(sol, u)
    cl = create_candidate_list(sol, u)
    alpha = alpha if alpha >= 0 else random.random()
    while not solution.is_feasible(sol):
        gmin, gmax = evalGminGmax(cl)
        th = gmax - alpha * (gmax - gmin)
        rcl = []
        for i in range(len(cl)):
            if cl[i][0] >= th:
                rcl.append(cl[i])
        selIdx = random.randint(0, len(rcl)-1)
        cSel = rcl[selIdx]
        solution.add_to_solution(sol, cSel[1], cSel[0])
        cl.remove(cSel)
        update_candidate_list(sol, cl, cSel[1])
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
            d = solution.distance_sum_to_solution(sol, c)
            cl.append([d, c])
    return cl


def evalGminGmax(cl: list) -> tuple:
    '''Evaluates the minimum and maximum sum of distances (first element in each tuple) between the
    candidate nodes (second element in each tuple).

    Args:
      cl (list): a list of candidate solutions. Each candidate solution is represented as a list
    containing the sum of the distances to the rest of the nodes in the solution and the index
    of the candidate solution.

    Returns:
      (tuple): contains two values: the minimum sum of distances between the elements in the input
    candidate list `cl` (gmin) and the maximum value (gmax).
    '''
    gmin = 0x3f3f3f3f  # Num. muy grande
    gmax = 0
    for c in cl:
        gmin = min(gmin, c[0])
        gmax = max(gmax, c[0])
    return gmin, gmax


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
        c[0] += sol['instance']['d'][added][c[1]]
