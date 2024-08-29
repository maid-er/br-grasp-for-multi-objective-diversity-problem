'''GRASP execution function (construction and LS calls)'''
from constructives import biased_randomized
from local_search import variable_neighborhood_descent
from structure.solution import Solution

from utils.logger import load_logger

logging = load_logger(__name__)


def execute(inst: dict, config: dict) -> Solution:
    '''The function executes a GRASP algorithm with a specified number of iterations and a given
    beta value, selecting the best solution found during the iterations.

    Args:
      inst (dict): a dictionary containing the instance data. The dictionary includes the number of
    nodes `n`, the number of nodes to be selected `p`, a distance matrix `d` representing the
    distances from each node to the rest of the nodes, a cost vector `a` with the costs of each
    node, and a capacity vector `a` with the capacities of each node.
      config (dict): contains the construction and local search strategies defined by the user in
    the config file.

    Returns:
        (Solution): the solution found.
    '''
    # Get config parameters
    parameters = config.get('parameters')
    ls_strategy = config.get('strategy')
    ls_scheme = config.get('scheme')

    logging.info('Executing GRASP algorithm with: ')
    logging.info('\tBiased construction with parameters %s', parameters)
    logging.info('\t%s Local Search strategy following the %s Improve scheme',
                 ls_strategy, ls_scheme)

    # Construction phase (Biased GRASP)
    sol = biased_randomized.construct(inst, parameters)
    logging.info("\tConstruction phase:")
    logging.info('\t\tMaxSum: %s', sol.of_MaxSum)
    logging.info('\t\tMaxMin: %s', sol.of_MaxMin)
    logging.info('Cost: %s, Capacity: %s', sol.total_cost, sol.total_capacity)

    # Local Search phase
    variable_neighborhood_descent.improve(sol, config)

    logging.info("\tLocal Search improvement phase:")
    logging.info('\t\tMaxSum: %s', sol.of_MaxSum)
    logging.info('\t\tMaxMin: %s', sol.of_MaxMin)
    logging.info('Cost: %s, Capacity: %s', sol.total_cost, sol.total_capacity)

    return sol
