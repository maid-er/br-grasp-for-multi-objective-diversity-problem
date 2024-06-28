'''Auxiliar functions to find non-dominated solutions'''
from structure.solution import Solution


def is_dominant(sol1: Solution, sol2: Solution) -> bool:
    '''
    Checks if `sol2` is dominated by `sol1`. A solution is dominated if another solution
    is no worse in all objectives and better in at least one.

    Args:
      sol1 (Solution): contains the objective function values of the solution 1.
      sol2 (Solution): contains the objective function values of the solution 2.

    Returns:
      (bool): indicates whether the `sol2` is dominated by `sol1`.
    '''
    if sol2:
        condition1 = all([sol2.of_MaxSum <= sol1.of_MaxSum,
                          sol2.of_MaxMin <= sol1.of_MaxMin])

        condition2 = any([sol2.of_MaxSum < sol1.of_MaxSum,
                          sol2.of_MaxMin < sol1.of_MaxMin])

        return condition1 and condition2
    return True


def get_nondominated_solutions(all_solutions: list) -> list:
    '''
    Identifies non-dominated solutions within a list of solutions.

    Args:
      all_solutions (list): solutions where each solution is represented as a Solution instance.

    Returns:
      (list of bool): each value indicates whether the corresponding solution in the input list
    `all_solutions` is non-dominated by any other solution in the list.
    '''
    is_non_dominated = [True] * len(all_solutions)
    for i, sol_i in enumerate(all_solutions):
        for j, sol_j in enumerate(all_solutions):
            if i != j and is_dominant(sol_j, sol_i):
                is_non_dominated[i] = False
                break

    return is_non_dominated
