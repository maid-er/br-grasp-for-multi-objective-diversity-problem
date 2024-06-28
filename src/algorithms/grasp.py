'''GRASP execution function (construction and LS calls)'''
from constructives import biased_randomized
from localsearch import best_improve, first_improve, variable_neighborhood_descent
from structure.solution import Solution

from utils.logger import load_logger

logging = load_logger(__name__)


def execute(inst: dict, config: dict) -> Solution:
    '''The function executes a GRASP algorithm with a specified number of iterations and a given
    alpha value, selecting the best solution found during the iterations.

    Args:
      inst (dict): a dictionary containing the instance data. The dictionary includes the number of
    nodes `n`, the number of nodes to be selected `p`, and a distance matrix `d` representing the
    distances from each node to the rest of the nodes.
      config (dict): contains the construction and local search strategies defined by the user in
    the config file.

    Returns:
        (Solution): the solution found.
    '''
    strategy = config.get('construction_method')
    parameters = config.get('parameters')

    logging.info('Executing GRASP algorithm with %s construction method and parameters %s',
                 strategy, parameters)

    sol = biased_randomized.construct(inst, parameters)
    logging.info("\tConstruction phase:")
    logging.info('\t\tMaxSum: %s', sol.of_MaxSum)
    logging.info('\t\tMaxMin: %s', sol.of_MaxMin)
    logging.info('Cost: %s, Capacity: %s', sol.total_cost, sol.total_capacity)

    ls_strategy = config.get('strategy')
    if ls_strategy == 'Best':
        best_improve.improve(sol)
    elif ls_strategy == 'First':
        first_improve.improve(sol)
    elif ls_strategy == 'VND':
        variable_neighborhood_descent.improve(sol)
    else:
        logging.error('Invalid Local Search strategy %s.', ls_strategy)
    logging.info("\tLocal Search improvement phase:")
    logging.info('\t\tMaxSum: %s', sol.of_MaxSum)
    logging.info('\t\tMaxMin: %s', sol.of_MaxMin)
    logging.info('Cost: %s, Capacity: %s', sol.total_cost, sol.total_capacity)

    return sol
