'''Auxiliar functions to construct greedy solution'''
from structure import solution


def construct(inst: dict):
    '''Constructs a solution by iteratively adding elements to it until it becomes feasible.

    Args:
      inst (dict): contains the instance data. The dictionary includes the number of nodes `n`,
    the number of nodes to be selected `p`, and a distance matrix `d` representing the distances
    from each node to the rest of the nodes.

    Returns:
      (dict): contains the solution information in three key-value pairs: 'sol' with the set
    of selected candidates for the solution, 'of' with the objective value, and 'instance' that
    contains the instance data, with key 'd' representing the distance matrix between all the
    candidate nodes.
    '''
    sol = solution.createEmptySolution(inst)
    u, v = findLargestDistance(inst)
    solution.addToSolution(sol, u)
    solution.addToSolution(sol, v)
    cl, pos = createCandidateList(sol)
    while not solution.isFeasible(sol):
        c = cl[pos][0]
        d = cl[pos][1]
        solution.addToSolution(sol, c, d)
        del cl[pos]
        pos = updateCandidateList(sol, cl, c)
    return sol


def findLargestDistance(inst: dict):
    '''Finds the pair of indices with the largest distance value in a given input dictionary.

    Args:
      inst (dict): contains the instance data. The dictionary includes the number of nodes `n`,
    the number of nodes to be selected `p`, and a distance matrix `d` representing the distances
    from each node to the rest of the nodes.

    Returns:
      (tuple): the indices of the two elements in the input dictionary `inst` that have the
    largest distance between them.
    '''
    n = inst['n']
    best1 = -1
    best2 = -1
    largest = 0
    for i in range(n):
        for j in range(i+1, n):
            if inst['d'][i][j] > largest:
                best1 = i
                best2 = j
                largest = inst['d'][i][j]
    return best1, best2


def createCandidateList(sol: dict):
    '''Generates a list of candidate solutions based on the input solution and returns the list
    along with the index of the best candidate.

    Args:
      sol (dict): contains the solution information in three key-value pairs: 'sol' with the set
    of selected candidates for the solution, 'of' with the objective value, and 'instance' that
    contains the instance data, with key 'd' representing the distance matrix between all the
    candidate nodes.

    Returns:
      (list): candidate solutions.
      (int): index of the best candidate solution.
    '''
    n = sol['instance']['n']
    cl = []
    largest = 0
    bestIndex = 0
    for c in range(n):
        if not solution.contains(sol, c):
            d = solution.distanceToSolution(sol, c)
            cl.append([c, d])
            if d > largest:
                largest = d
                bestIndex = len(cl)-1
    return cl, bestIndex


def updateCandidateList(sol: dict, cl: list, added: int) -> int:
    '''This function updates a candidate list by calculating the best index based on certain 
    criteria.

    Args:
      sol (dict): contains the solution information in three key-value pairs: 'sol' with the set
    of selected candidates for the solution, 'of' with the objective value, and 'instance' that
    contains the instance data, with key 'd' representing the distance matrix between all the
    candidate nodes.
      cl (list): a list of candidate solutions. Each candidate solution is represented as a list
    containing the sum of the distances to the rest of the nodes in the solution and the index
    of the candidate solution.
      added (int): represents the ID of the candidate that was added to the solution.

    Returns:
      (int): the index of the candidate with the highest sum of distances after updating the
    score based on the given solution and the newly added item.
    '''
    bestIndex = 0
    largest = 0
    for i in range(len(cl)):
        c = cl[i]
        c[1] += sol['instance']['d'][added][c[0]]
        if c[1] > largest:
            bestIndex = i
            largest = c[1]
    return bestIndex
