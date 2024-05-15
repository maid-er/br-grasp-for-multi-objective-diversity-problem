'''Main function'''
import datetime
import matplotlib.pyplot as plt
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
    inst = instance.readInstance(path)
    sol = grasp.execute(inst, 100, -1)
    solution.printSol(sol)


def executeDir():
    dir = "instances/USCAP"
    with os.scandir(dir) as files:
        ficheros = [file.name for file in files if file.is_file() and file.name.endswith(".txt")]

    result_table = pd.DataFrame(columns=['Solution', 'MaxSum', 'MaxMin', 'Cost', 'Capacity'])

    for f in ficheros:
        for _ in range(8):
            path = os.path.join(dir, f)
            logging.info('Solving instance %s:', f)
            inst = instance.read_USCAP_instance(path)
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

                selected_nodes = ' - '.join([str(s+1) for s in sol['sol']])
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

        result_table.to_csv(f'results_{dir}.csv', index=False)
        result_table.plot.scatter(x='MaxSum', y='MaxMin')
        plt.show()


if __name__ == '__main__':
    logging.info('Initializing diversity maximization algorithm...')
    # executeInstance()
    executeDir()
