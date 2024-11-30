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
    # Initialize list and table to save solutions
    all_solutions = []
    result_table = pd.DataFrame(columns=['Solution', 'MaxSum', 'MaxMin', 'Cost', 'Capacity'])

    print('Solving instance %s:', path)
    # Read instance
    inst = instance.read_instance(path)

    max_time = config.get('execution_limits').get('max_time')
    start = datetime.datetime.now()
    # Construct a solution for the IT defined in config
    for i in range(config.get('iterations')):
        # If time is exceeded stop execution
        if datetime.timedelta(seconds=max_time) < datetime.datetime.now() - start:
            print('Maximum allowed execution time is exceeded. Total IT: %s', i)
            break

        # Define objective considered in this IT
        construction_approach = config.get('mo_approach_C')
        objective = i % 2  # 0: MaxSum, 1: MaxMin (for default AltBwC approach)

        # Check if a single objective approach have been defined
        if construction_approach == 'MaxSum':
            objective = 0
        elif construction_approach == 'MaxMin':
            objective = 1

        # Run B-GRASP-VND
        print(f'Finding solution #{i+1}')
        solution_list = grasp.execute(inst, config, objective)
        # Save solution set found in this IT
        all_solutions += solution_list

        # Add new solutions to result_table
        for sol in solution_list:
            selected_nodes = ' - '.join([str(s) for s in sorted(sol.solution_list)])
            result_table.loc[len(result_table)] = [selected_nodes] + [sol.of_MaxSum,
                                                                      sol.of_MaxMin,
                                                                      sol.total_cost,
                                                                      sol.total_capacity]

    # Find non-dominated solutions among all constructions
    is_non_dominated = dominance.get_nondominated_solutions(all_solutions)
    result_table = result_table[is_non_dominated].reset_index(drop=True)

    # Compute execution time
    elapsed = datetime.datetime.now() - start
    secs = round(elapsed.total_seconds(), 2)
    print('Execution time: %s', secs)
    add_data = {
        'time': [secs],
        'all_sols': [len(all_solutions)],
        'nd_sols': [len(result_table)]
    }

    # Build and plot Pareto Front
    fig = results.pareto_front(result_table, path)
    # Save table and plot with results
    algorithm_params = (f'IT{config.get("iterations")}'
                        f'_b{config.get("parameters").get("beta")}'
                        f'_{config.get("scheme")[:3]}'
                        # f'_nb{len(config.get("neighborhoods"))}'
                        ).replace('.', '')
    results.save(result_table, add_data, fig, algorithm_params, path)


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
