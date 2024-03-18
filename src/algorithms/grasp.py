'''GRASP execution function (construction and LS calls)'''
from constructives import greedy, cgrasp, biased_randomized
from localsearch import lsfirstimprove, lsbestimprove


def execute(inst: dict, iters: int, strategy: str, alpha: float) -> dict:
    '''The function executes a GRASP algorithm with a specified number of iterations and a given
    alpha value, selecting the best solution found during the iterations.

    Args:
      inst (dict): a dictionary containing the instance data. The dictionary includes the number of
    nodes `n`, the number of nodes to be selected `p`, and a distance matrix `d` representing the
    distances from each node to the rest of the nodes.
      iters (int): represents the number of iterations or loops that the algorithm will run. It
    determines how many times the algorithm will execute the construction and improvement steps
    before returning the best solution found.
      alpha (float): it is a parameter used in the construction phase of the GRASP algorithm. It
    controls the level of randomness in the construction of initial solutions. A higher alpha value
    leads to more randomness, while a lower alpha value results in less randomness. It is typically
    a value between 0 and 1.

    Returns:
        (dict): the best solution found after running a specified number of iterations. The best
    solution is determined based on the objective function value (`of`) of each solution generated
    during the iterations. Contains the solution information in three key-value pairs: 'sol' with
    the set of selected candidates for the solution, 'of' with the objective value, and 'instance'
    that contains the instance data, with key 'd' representing the distance matrix between all the
    candidate nodes.
    '''
    best = None
    for i in range(iters):
        print("IT " + str(i + 1))
        if strategy == 'Restricted list':
            sol = cgrasp.construct(inst, alpha)
        elif strategy == 'Biased Randomized':
            sol = biased_randomized.construct(inst, 'Geometric', alpha)
        else:
            sol = greedy.construct(inst)
        print("\tC: "+str(sol['of']))
        # lsfirstimprove.improve(sol)
        lsbestimprove.improve(sol)
        print("\tLS: " + str(sol['of']))
        if best is None or best['of'] < sol['of']:
            best = sol
        print("\tB: " + str(best['of']))
    return best
