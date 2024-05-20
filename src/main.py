'''Main function'''
import datetime
import plotly.express as px
import os
import pandas as pd
import random

from structure import solution, instance
from algorithms import grasp

from utils.config import read_config
from utils.logger import load_logger

logging = load_logger(__name__)

config = read_config('config')


def executeInstance():
    random.seed(1309)
    path = "instances/preliminar/MDG-a_1_100_m10.txt"
    inst = instance.read_instance(path)
    sol = grasp.execute(inst, 100, config[0])
    solution.printSol(sol)


def executeDir():
    all_solutions = []
    dir = "instances/GDP"
    with os.scandir(dir) as files:
        ficheros = [file.name for file in files if file.is_file() and file.name.endswith(".txt")]

    result_table = pd.DataFrame(columns=['Solution', 'MaxSum', 'MaxMin', 'Cost', 'Capacity'])

    for f in ficheros:
        logging.info('Solving instance %s:', f)
        for i in range(20):
            path = os.path.join(dir, f)
            logging.info(f'Finding solution #{i+1}')
            inst = instance.read_instance(path)
            for method_config in config:
                start = datetime.datetime.now()
                sol = grasp.execute(inst, 100, method_config)
                elapsed = datetime.datetime.now() - start
                secs = round(elapsed.total_seconds(), 2)
                logging.info('MaxSum objective function value for the best result: %s',
                             sol['of_MaxSum'])
                logging.info('MaxMin objective function value for the best result: %s',
                             sol['of_MaxMin'])
                logging.info('Execution time: %s', secs)

                all_solutions.append(sol)

                selected_nodes = ' - '.join([str(s+1) for s in sorted(sol['sol'])])
                result_table.loc[len(result_table)] = [selected_nodes] + [sol.get(key)
                                                                          for key in [
                                                                              'of_MaxSum',
                                                                              'of_MaxMin',
                                                                              'total_cost',
                                                                              'total_capacity']]

            logging.info('Final solution:')
            logging.info('Selected elements: %s', sol['sol'])
            logging.info('MaxSum objective function value for the best result: %s',
                         sol['of_MaxSum'])
            logging.info('MaxMin objective function value for the best result: %s',
                         sol['of_MaxMin'])
            logging.info('Cost: %s, Capacity: %s', sol['total_cost'], sol['total_capacity'])

        fig = px.scatter(result_table, x='MaxMin', y='MaxSum', color='Solution')
        fig.show()

        is_non_dominated = solution.get_nondominated_solutions(all_solutions)
        result_table = result_table[is_non_dominated].reset_index(drop=True)
        result_table.to_csv(f'results_{f.split(".")[0]}.csv', index=False)

        fig = px.scatter(result_table, x='MaxMin', y='MaxSum', color='Solution')
        fig.show()


if __name__ == '__main__':
    logging.info('Initializing diversity maximization algorithm...')
    # executeInstance()
    executeDir()
