'''Main function'''
import datetime
import os
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
    dir = "instances/preliminar"
    with os.scandir(dir) as files:
        ficheros = [file.name for file in files if file.is_file() and file.name.endswith(".txt")]

    with open('resultados.csv', "w") as results:
        # results.write(
        #     'instance,RL_01,RL_03,RL_05,RL_07,RL_09,BR_T,BR_G_01,BR_G_03,BR_G_05,BR_G_07,BR_G_09,\n'
        #     )
        results.write(
            'instance,BR_T_MaxSum,BR_T_MaxMin,\n'
        )
        for f in ficheros:
            path = os.path.join(dir, f)
            logging.info('Solving instance %s:', f)
            inst = instance.readInstance(path)
            results.write(f + ',')
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
                results.write(str(round(sol['of_MaxSum'], 2)) + ',')
                results.write(str(round(sol['of_MaxMin'], 2)) + ',')

            results.write('\n')


if __name__ == '__main__':
    logging.info('Initializing diversity maximization algorithm...')
    # executeInstance()
    executeDir()
