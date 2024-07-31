import datetime
import os
import pandas as pd

from algorithms import grasp
from structure import instance, dominance

from utils.results import OutputHandler
from utils.logger import load_logger

logging = load_logger(__name__)


def execute_instance(path: str, config: dict, results: OutputHandler):

    all_solutions = []
    result_table = pd.DataFrame(columns=['Solution', 'MaxSum', 'MaxMin', 'Cost', 'Capacity'])

    logging.info('Solving instance %s:', path)
    # Read instance
    inst = instance.read_instance(path)

    start = datetime.datetime.now()
    for i in range(config.get('iterations')):
        # Construct a solution for each iteration
        logging.info(f'Finding solution #{i+1}')
        sol = grasp.execute(inst, config)
        all_solutions.append(sol)

        logging.info('MaxSum objective function value for the best result: %s', sol.of_MaxSum)
        logging.info('MaxMin objective function value for the best result: %s', sol.of_MaxMin)

        selected_nodes = ' - '.join([str(s+1) for s in sorted(sol.solution_set)])
        result_table.loc[len(result_table)] = [selected_nodes] + [sol.of_MaxSum,
                                                                  sol.of_MaxMin,
                                                                  sol.total_cost,
                                                                  sol.total_capacity]

        logging.info('Final solution:')
        logging.info('Selected elements: %s', sol.solution_set)
        logging.info('MaxSum objective function value for the best result: %s', sol.of_MaxSum)
        logging.info('MaxMin objective function value for the best result: %s', sol.of_MaxMin)
        logging.info('Cost: %s, Capacity: %s', sol.total_cost, sol.total_capacity)

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
                        f'_beta{config.get("parameters").get("beta")}'
                        f'_LS{config.get("scheme")}')
    results.save(result_table, fig, algorithm_params, path)

    return secs


def execute_directory(directory: str, config: dict):
    with os.scandir(directory) as files:
        ficheros = [file.name for file in files if file.is_file() and file.name.endswith(".txt")]

    experiments_table = pd.DataFrame(columns=['Instance', 'Execution time'])

    results = OutputHandler()

    for f in ficheros:
        path = os.path.join(directory, f)
        for method_config in config:
            execution_time = execute_instance(path, method_config, results)

            experiments_table.loc[len(experiments_table)] = [f.split('.')[0], execution_time]

            algorithm_params = (f'IT{method_config.get("iterations")}'
                                f'_beta{method_config.get("parameters").get("beta")}'
                                f'_LS{method_config.get("scheme")}')
            experiments_table.to_csv(
                os.path.join('output', f'{algorithm_params}_{results.execution_n}.csv'),
                index=False)
