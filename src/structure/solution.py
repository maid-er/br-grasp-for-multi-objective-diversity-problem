'''Auxiliar function to handle candidate solutions'''


def createEmptySolution(instance: dict) -> dict:
    '''The function creates an empty solution dictionary with keys 'sol', 'of', and 'instance'.

    Args:
      instance (dict): a dictionary containing the instance data. The dictionary includes the
    number of nodes `n`, the number of nodes to be selected `p`, and a distance matrix `d`
    representing the sum of the distances from each node to the rest of the nodes.

    Returns:
      (dict): contains three key-value pairs: 'sol' with an empty set, 'of' with a value of 0,
    and 'instance' with the input parameter `instance`.
    '''
    solution = {}
    solution['sol'] = set()
    solution['of'] = 0
    solution['instance'] = instance
    return solution


def evaluate(sol: dict) -> float:
    '''Evaluates a solution based on a given instance by calculating the objective function value.

    Args:
      sol (dict): contains the solution information in three key-value pairs: 'sol' with the set
    of selected candidates for the solution, 'of' with the objective value, and 'instance' that
    contains the instance data, with key 'd' representing the distance matrix between all the
    candidate nodes.

    Returns:
      (float): objective function value (of) calculated based on the solution provided in the 'sol'
    key of the input dictionary 'sol'. The objective function value is computed by iterating over
    pairs of elements in the solution and summing the distances between them as specified in the 'd'
    key of the 'instance' dictionary within the 'sol' dictionary.
    '''
    of = 0
    for s1 in sol['sol']:
        for s2 in sol['sol']:
            if s1 < s2:
                of += sol['instance']['d'][s1][s2]
    return of


def addToSolution(sol: dict, u: int, ofVariation: float = -1):
    '''Updates a solution by adding a specified element and its corresponding value to the objective
    function.

    Args:
      sol (dict): contains the solution information in three key-value pairs: 'sol' with the set
    of selected candidates for the solution, 'of' with the objective value, and 'instance' that
    contains the instance data, with key 'd' representing the distance matrix between all the
    candidate nodes.
      u (int): represents the ID of an element (node) that will be added to the solution.
      ofVariation (float): is an optional parameter with a default value of -1. The default value
    -1 is used when the first candidate is added to sum all the distances from selected candidate
    `u` to the rest of the candidates in the objective function 'of'. Then, each time a new
    candidate is added, the `ofVariation` is received as an input representing the sum of the
    distances from the added element `u` and the rest of the nodes in the solution.
    '''
    if ofVariation == -1:
        for s in sol['sol']:
            sol['of'] += sol['instance']['d'][u][s]
    else:
        sol['of'] += ofVariation
    sol['sol'].add(u)


def removeFromSolution(sol: dict, u: int, ofVariation: float = -1):
    '''Removes an element from a solution and updates the objective function value accordingly.

    Args:
      sol (dict): contains the solution information in three key-value pairs: 'sol' with the set
    of selected candidates for the solution, 'of' with the objective value, and 'instance' that
    contains the instance data, with key 'd' representing the distance matrix between all the
    candidate nodes.
      u (int): represents the ID of an element (node) that will be removed from the solution.
      ofVariation (): ????????
    '''
    sol['sol'].remove(u)
    if ofVariation == -1:
        for s in sol['sol']:
            sol['of'] -= sol['instance']['d'][u][s]
    else:
        sol['of'] -= ofVariation


def contains(sol: dict, u: int) -> bool:
    '''Checks if a given candidate ID `u` is present in the current solution dictionary `sol` under
    the key 'sol'.

    Args:
      sol (dict): contains the solution information in three key-value pairs: 'sol' with the set
    of selected candidates for the solution, 'of' with the objective value, and 'instance' that
    contains the instance data, with key 'd' representing the distance matrix between all the
    candidate nodes.
      u (int): represents the ID of a candidate element (node).

    Returns:
      (bool): indicates whether the variable `u` is present in the 'sol' key of the dictionary
    `sol`.
    '''
    return u in sol['sol']


def distanceSumToSolution(sol: dict, u: int, without: int = -1) -> float:
    '''Calculates the sum of the distances from a given node to the rest of the nodes in the
    solution graph, excluding the node specified with the optional input `without`.

    Args:
      sol (dict): contains the solution information in three key-value pairs: 'sol' with the set
    of selected candidates for the solution, 'of' with the objective value, and 'instance' that
    contains the instance data, with key 'd' representing the distance matrix between all the
    candidate nodes.
      u (int): represents the ID of the candidate element (node) from which we want to calculate
    the sum of the distances to the rest of the nodes.
      without (int): it is an optional parameter that allows you to specify the ID of the node that
    should be excluded from the calculation of the sum of the distances. If the `without` parameter
    is provided, the function will skip calculating the distance to the specified value in the
    solution.

    Returns:
      (float): returns the sum of the distances from a given node `u` to the rest of the nodes in
    solution `sol`, excluding the distance to a specific node `without` if provided.
    '''
    d = 0
    for s in sol['sol']:
        if s != without:
            d += sol['instance']['d'][s][u]
    return round(d, 2)


def minimumDistanceToSolution(sol: dict, u: int, without: int = -1) -> float:
    '''Calculates the minimum distance from a given node to the rest of the nodes in the
    solution graph, excluding the node specified with the optional input `without`.

    Args:
      sol (dict): contains the solution information in three key-value pairs: 'sol' with the set
    of selected candidates for the solution, 'of' with the objective value, and 'instance' that
    contains the instance data, with key 'd' representing the distance matrix between all the
    candidate nodes.
      u (int): represents the ID of the candidate element (node) from which we want to find the
    minimum distance to the rest of the nodes.
      without (int): it is an optional parameter that allows you to specify the ID of the node that
    should be excluded from the search of the minimum distance. If the `without` parameter
    is provided, the function will skip calculating the distance to the specified value in the
    solution.

    Returns:
      (float): returns the minimum distance value from a given node `u` to the rest of the nodes in
    solution `sol`, excluding the distance to a specific node `without` if provided.
    '''
    min_d = 0x3f3f3f3f
    for s in sol['sol']:
        if s != without:
            d = sol['instance']['d'][s][u]
            if d < min_d:
                min_d = d
    return round(min_d, 2)


def isFeasible(sol: dict) -> float:
    '''Checks if a solution has the same number of elements specified in the instance parameter `p`.

    Args:
      sol (dict): contains the solution information in three key-value pairs: 'sol' with the set
    of selected candidates for the solution, 'of' with the objective value, and 'instance' that
    contains the instance data, with key 'd' representing the distance matrix between all the
    candidate nodes.

    Returns:
      (bool): indicates whether the length of the 'sol' key in the input dictionary 'sol', that is,
    the selected candidates in the solution, is equal to the required number of selected elements
    'p' in the 'instance'.
    '''
    return len(sol['sol']) == sol['instance']['p']


def printSol(sol: dict):
    '''Prints the solution.

    Args:
      sol (dict): contains the solution information in three key-value pairs: 'sol' with the set
    of selected candidates for the solution, 'of' with the objective value, and 'instance' that
    contains the instance data, with key 'd' representing the distance matrix between all the
    candidate nodes.
    '''
    print("SOL: "+str(sol['sol']))
    print("OF: "+str(round(sol['of'], 2)))
