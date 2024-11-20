'''Directory and instance execution auxiliar functions'''
import datetime
import os
import pandas as pd

from algorithms import grasp
from structure import instance, dominance

from utils.results import OutputHandler
from utils.logger import load_logger

logging = load_logger(__name__)


def execute_instance(path: str, config: dict, results: OutputHandler) -> float:
    '''
    Reads an instance, iterates to find solutions using GRASP algorithm, evaluates the solutions,
    identifies non-dominated solutions, computes execution time, and saves results.

    Args:
      path (str): represents the path to the instance that needs to be solved. This path is used
    to read the instance data and save the results later on with the same name.
      config (dict): contains the configuration settings for the algorithm.
      results (OutputHandler): contains methods for handling and displaying the output of the
    algorithm, such as generating plots and saving results to files with the ID number of the
    execution number of each instance.

    Returns:
      (float): returns the total execution time in seconds.
    '''
    all_solutions = []
    result_table = pd.DataFrame(columns=['Solution', 'MaxSum', 'MaxMin', 'Cost', 'Capacity'])

    logging.info('Solving instance %s:', path)
    # Read instance
    inst = instance.read_instance(path)

    max_time = config.get('execution_limits').get('max_time')
    start = datetime.datetime.now()
    for i in range(config.get('iterations')):
        # If time is exceeded stop execution
        if datetime.timedelta(seconds=max_time) < datetime.datetime.now() - start:
            logging.info('Maximum allowed execution time is exceeded. Total IT: %s', i)
            break
        # Construct a solution for each iteration
        logging.info(f'Finding solution #{i+1}')
        solution_set = grasp.execute(inst, config)
        # all_solutions.append(sol)
        all_solutions += solution_set

        # logging.info('MaxSum objective function value for the best result: %s', sol.of_MaxSum)
        # logging.info('MaxMin objective function value for the best result: %s', sol.of_MaxMin)

        for sol in solution_set:
            selected_nodes = ' - '.join([str(s) for s in sorted(sol.solution_set)])
            result_table.loc[len(result_table)] = [selected_nodes] + [sol.of_MaxSum,
                                                                      sol.of_MaxMin,
                                                                      sol.total_cost,
                                                                      sol.total_capacity]

        # logging.info('Final solution:')
        # logging.info('Selected elements: %s', sol.solution_set)
        # logging.info('MaxSum objective function value for the best result: %s', sol.of_MaxSum)
        # logging.info('MaxMin objective function value for the best result: %s', sol.of_MaxMin)
        # logging.info('Cost: %s, Capacity: %s', sol.total_cost, sol.total_capacity)

    # Find non-dominated solutions among all constructions
    is_non_dominated = dominance.get_nondominated_solutions(all_solutions)
    result_table = result_table[is_non_dominated].reset_index(drop=True)

    # Compute execution time
    elapsed = datetime.datetime.now() - start
    secs = round(elapsed.total_seconds(), 2)
    logging.info('Execution time: %s', secs)

    # Build and plot Pareto Front
    fig = results.pareto_front(result_table, path)
    # Save table and plot with results
    algorithm_params = (f'IT{config.get("iterations")}'
                        f'_b{config.get("parameters").get("beta")}'
                        f'_{config.get("scheme")[:3]}'
                        # f'_nb{len(config.get("neighborhoods"))}'
                        ).replace('.', '')
    results.save(result_table, secs, fig, algorithm_params, path)


def execute_directory(directory: str, config: dict):
    '''
    Scans a directory for text files, executes instances with specified configurations, and saves
    the results in a CSV file.

    Args:
      directory (str): represents the path to the directory where the files (instances) are located.
      config (dict): contains the configuration settings for the algorithm.
    '''
    with os.scandir(directory) as files:
        ficheros = [file.name for file in files if file.is_file() and file.name.endswith(".txt")]

    results = OutputHandler()

    for f in ficheros:
        path = os.path.join(directory, f)
        execute_instance(path, config, results)
