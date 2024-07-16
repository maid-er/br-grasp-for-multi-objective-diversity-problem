import datetime
import os
import pandas as pd

from algorithms import grasp
from structure import instance, dominance

from utils import results
from utils.logger import load_logger

logging = load_logger(__name__)


def execute_instance(path, config):

    all_solutions = []
    result_table = pd.DataFrame(columns=['Solution', 'MaxSum', 'MaxMin', 'Cost', 'Capacity'])

    logging.info('Solving instance %s:', path)
    # Read instance
    inst = instance.read_instance(path)
    for method_config in config:
        start = datetime.datetime.now()
        for i in range(method_config.get('iterations')):
            # Construct a solution for each iteration
            logging.info(f'Finding solution #{i+1}')
            sol = grasp.execute(inst, method_config)
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
        # Build and plot Pareto Front
        fig = results.pareto_front(result_table, path)
        # Save table and plot with results
        results.save(result_table, fig, path)

        # Compute execution time
        elapsed = datetime.datetime.now() - start
        secs = round(elapsed.total_seconds(), 2)
        logging.info('Execution time: %s', secs)


def execute_directory(directory, config):
    with os.scandir(directory) as files:
        ficheros = [file.name for file in files if file.is_file() and file.name.endswith(".txt")]

    for f in ficheros:
        path = os.path.join(directory, f)
        execute_instance(path, config)
