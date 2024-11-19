'''Main function'''
import os

from utils import execution
from utils.config import read_config
from utils.logger import load_logger

logging = load_logger(__name__)

config_list = read_config('config')


if __name__ == '__main__':
    logging.info('Initializing diversity maximization algorithm...')

    path = os.path.join(os.getcwd(),'instances', 'GDP_test', 'GKD-b_n50')
    path2 = "C:/Users/Antor/Desktop/DOC PAPERS/Multi objective DP/br-grasp-for-multi-objective-diversity-problem/instances/GDP_test/GKD-b_n50"

    for config in config_list:
        # execution.execute_instance(path, config)
        for n in range(1):
            execution.execute_directory(path2, config)

        os.remove(os.path.join('temp', 'execution.txt'))
