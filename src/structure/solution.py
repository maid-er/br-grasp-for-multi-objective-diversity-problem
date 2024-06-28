'''Auxiliar function to handle candidate solutions'''


def create_empty_solution(instance: dict) -> dict:
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
    solution['of_MaxSum'] = 0
    solution['of_MaxMin'] = 0x3f3f3f3f
    solution['total_cost'] = 0
    solution['total_capacity'] = 0
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


def add_to_solution(sol: dict, u: int, min_distance: float = -1, sum_variation: float = -1):
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
    if sum_variation == -1 or min_distance == -1:
        for s in sol['sol']:
            distance_u_s = sol['instance']['d'][u][s]
            sol['of_MaxSum'] += distance_u_s
            if sol['of_MaxMin'] > distance_u_s:
                sol['of_MaxMin'] = distance_u_s
    else:
        sol['of_MaxSum'] += sum_variation
        if sol['of_MaxMin'] > min_distance:
            sol['of_MaxMin'] = min_distance
    sol['total_cost'] += sol['instance']['a'][u]
    sol['total_capacity'] += sol['instance']['c'][u]
    sol['sol'].add(u)


def remove_from_solution(sol: dict, u: int, sum_variation: float = -1):
    '''Removes an element from a solution and updates the objective function value accordingly.

    Args:
      sol (dict): contains the solution information in three key-value pairs: 'sol' with the set
    of selected candidates for the solution, 'of' with the objective value, and 'instance' that
    contains the instance data, with key 'd' representing the distance matrix between all the
    candidate nodes.
      u (int): represents the ID of an element (node) that will be removed from the solution.
      ofVariation (float): is an optional parameter with a default value of -1. Each time a node
    is removed from the solution, the `ofVariation` is received as an input representing the sum
    of the distances from the removed element `u` and the rest of the nodes in the solution.
    '''
    sol['sol'].remove(u)
    if sum_variation == -1:
        for s in sol['sol']:
            sol['of_MaxSum'] -= sol['instance']['d'][u][s]
    else:
        sol['of_MaxSum'] -= sum_variation
    sol['total_cost'] -= sol['instance']['a'][u]
    sol['total_capacity'] -= sol['instance']['c'][u]


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


def distance_sum_to_solution(sol: dict, u: int, without: int = -1) -> float:
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


def minimum_distance_to_solution(sol: dict, u: int, without: int = -1) -> float:
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
        if s != without and s != u:
            d = sol['instance']['d'][s][u]
            if d < min_d:
                min_d = d
    return round(min_d, 2)


def is_feasible(sol: dict) -> float:
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
    # return len(sol['sol']) == sol['instance']['p']
    return len(sol['sol']) > 1


def satisfies_cost(sol: dict, u: int, v: int = -1):
    # removing_candidate = 0
    # if v != -1:
    #     removing_candidate = sol['instance']['a'][v]
    possible_cost = sol['total_cost']
    if v != -1:
        for q in v:
            possible_cost -= sol['instance']['a'][q]
    for q in u:
        possible_cost += sol['instance']['a'][q]

    return possible_cost < sol['instance']['K']


def satisfies_capacity(sol: dict, u: int = -1, v: int = -1):
    # new_candidate = 0
    # if u != -1:
    #     new_candidate = sol['instance']['c'][u]
    # removing_candidate = 0
    # if v != -1:
    #     removing_candidate = sol['instance']['c'][v]
    possible_capacity = sol['total_capacity']
    if v != -1:
        for q in v:
            possible_capacity -= sol['instance']['c'][q]
    if u != -1:
        for q in u:
            possible_capacity += sol['instance']['c'][q]

    return possible_capacity > sol['instance']['B']


def is_dominant(new_sol: dict, best_sol: dict):
    '''
    Checks if `best_sol` is dominated by `new_sol`. A solution is dominated if another solution
    is no worse in all objectives and better in at least one.
    '''
    if best_sol:
        condition1 = all([best_sol['of_MaxSum'] <= new_sol['of_MaxSum'],
                          best_sol['of_MaxMin'] <= new_sol['of_MaxMin']])

        condition2 = any([best_sol['of_MaxSum'] < new_sol['of_MaxSum'],
                          best_sol['of_MaxMin'] < new_sol['of_MaxMin']])

        return condition1 and condition2
    return True


def print_sol(sol: dict):
    '''Prints the solution.

    Args:
      sol (dict): contains the solution information in three key-value pairs: 'sol' with the set
    of selected candidates for the solution, 'of' with the objective value, and 'instance' that
    contains the instance data, with key 'd' representing the distance matrix between all the
    candidate nodes.
    '''
    print(f"SOL: {sol['sol']}")
    print(f"OF MaxSum: {round(sol['of_MaxSum'], 2)}")
    print(f"OF MaxMin: {round(sol['of_MaxMin'], 2)}")
    print(f"Total cost: {round(sol['total_cost'], 2)}")
    print(f"Total capacity: {round(sol['total_capacity'], 2)}")


def get_nondominated_solutions(all_solutions: list):
    is_non_dominated = [True] * len(all_solutions)
    for i, sol_i in enumerate(all_solutions):
        for j, sol_j in enumerate(all_solutions):
            if i != j and is_dominant(sol_j, sol_i):
                is_non_dominated[i] = False
                break

    return is_non_dominated
