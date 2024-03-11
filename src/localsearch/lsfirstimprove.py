'''
Auxiliar function to apply First Improve Local Search.
Objective functions of ramdomly sorted selected and unselected elements are compared,
when the unselected element's result improves the selected one's, they are interchanged
in the solution.
'''
import random

from structure import solution


def improve(sol: dict):
    '''Iteratively tries to improve a solution until no further improvements can be made.

    Args:
      sol (dict): contains the solution information in three key-value pairs: 'sol' with the set
    of selected candidates for the solution, 'of' with the objective value, and 'instance' that
    contains the instance data, with key 'd' representing the distance matrix between all the
    candidate nodes.
    '''
    improve = True
    while improve:
        improve = tryImprove(sol)


def tryImprove(sol: dict) -> bool:
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
    selected, unselected = createSelectedUnselected(sol)
    random.shuffle(selected)
    random.shuffle(unselected)
    for s in selected:
        ds = solution.distanceToSolution(sol, s)
        for u in unselected:
            du = solution.distanceToSolution(sol, u, s)
            if du > ds:
                solution.removeFromSolution(sol, s)
                solution.addToSolution(sol, u)
                return True
    return False


def createSelectedUnselected(sol: dict):
    '''Takes a solution dictionary as input and returns two lists - one containing selected items
    and the other containing unselected items based on the solution.

    Args:
      sol (dict): contains the solution information in three key-value pairs: 'sol' with the set
    of selected candidates for the solution, 'of' with the objective value, and 'instance' that
    contains the instance data, with key 'd' representing the distance matrix between all the
    candidate nodes.

    Returns:
      selected (list): contains the candidates selected in the current solution.
      unselected (list): contains the unselected candidates in the current solution.
    '''
    selected = []
    unselected = []
    n = sol['instance']['n']
    for v in range(n):
        if solution.contains(sol, v):
            selected.append(v)
        else:
            unselected.append(v)
    return selected, unselected
