'''GRASP execution function (construction and LS calls)'''
from constructives import greedy, cgrasp, biased_randomized
from localsearch import lsbestimprove, variable_neighborhood_descent
from structure import solution

from utils.logger import load_logger

logging = load_logger(__name__)


def execute(inst: dict, iters: int, config: dict) -> dict:
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
    strategy = config.get('construction_method')
    parameters = config.get('parameters')

    logging.info('Executing GRASP algorithm with %s construction method and parameters %s',
                 strategy, parameters)

    best = None
    for i in range(iters):
        logging.info("IT %s", i + 1)
        if strategy == 'Restricted list':
            sol = cgrasp.construct(inst, parameters)
        elif strategy == 'Biased Randomized':
            sol = biased_randomized.construct(inst, parameters)
        else:
            sol = greedy.construct(inst)
        logging.info("\tConstruction phase:")
        logging.info('\t\tMaxSum: %s', sol['of_MaxSum'])
        logging.info('\t\tMaxMin: %s', sol['of_MaxMin'])
        logging.info('Cost: %s, Capacity: %s', sol['total_cost'], sol['total_capacity'])

        variable_neighborhood_descent.improve(sol)
        logging.info("\tLocal Search improvement phase:")
        logging.info('\t\tMaxSum: %s', sol['of_MaxSum'])
        logging.info('\t\tMaxMin: %s', sol['of_MaxMin'])
        logging.info('Cost: %s, Capacity: %s', sol['total_cost'], sol['total_capacity'])
        if solution.is_dominant(sol, best):
            best = sol
        logging.info("\tBest result so far:")
        logging.info('\t\tMaxSum: %s', best['of_MaxSum'])
        logging.info('\t\tMaxMin: %s', best['of_MaxMin'])
        logging.info('Cost: %s, Capacity: %s', sol['total_cost'], sol['total_capacity'])
    return best
