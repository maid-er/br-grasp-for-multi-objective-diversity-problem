'''
Auxiliar function to apply Best Improve Local Search.
The worst selected element and best unselected element are interchanged to improve
the initial solution.
'''
from structure import solution


def improve(sol: dict, maxIter: int = 50):
    '''Iteratively tries to improve a solution until no further improvements can be made.

    Args:
      sol (dict): contains the solution information in three key-value pairs: 'sol' with the set
    of selected candidates for the solution, 'of' with the objective value, and 'instance' that
    contains the instance data, with key 'd' representing the distance matrix between all the
    candidate nodes.
    '''
    count = 0
    while count < maxIter:
        improve = tryImprove(sol)
        if not improve:
            count += 1


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
    sel, ofVarSumSel, ofMinSel, unSel, ofVarSumUnsel, ofMinUnsel = selectInterchange(sol)
    if ofVarSumSel < ofVarSumUnsel and ofMinSel < ofMinUnsel:
        solution.addToSolution(sol, sel, ofMinSel, ofVarSumSel)
        solution.removeFromSolution(sol, unSel, ofMinUnsel, ofVarSumUnsel)
        return True
    return False


def selectInterchange(sol: dict):
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
    bestSumSel = 0x3f3f3f3f
    bestMinSel = 0x3f3f3f3f
    unsel = -1
    bestSumUnsel = 0
    bestMinUnsel = 0
    for v in sol['sol']:
        d_sum = solution.distanceSumToSolution(sol, v)
        d_min = solution.minimumDistanceToSolution(sol, v)
        if d_sum < bestSumSel and d_min < bestMinSel:
            bestSumSel = d_sum
            bestMinSel = d_min
            sel = v
    for v in range(n):
        if not solution.contains(sol, v):
            d_sum = solution.distanceSumToSolution(sol, v, without=sel)
            d_min = solution.minimumDistanceToSolution(sol, v, without=sel)
            if d_sum > bestSumUnsel and d_min > bestMinSel:
                bestSumUnsel = d_sum
                bestMinUnsel = d_min
                unsel = v
    return sel, bestSumSel, bestMinUnsel, unsel, bestSumUnsel, bestMinUnsel
