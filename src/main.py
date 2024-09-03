'''Main function'''
import os

from utils import execution
from utils.config import read_config
from utils.logger import load_logger

logging = load_logger(__name__)

config_list = read_config('config')


if __name__ == '__main__':
    logging.info('Initializing diversity maximization algorithm...')

    path = os.path.join('instances', 'GDP_test', 'GKD-b_n50')

    for config in config_list:
        # execution.execute_instance(path, config)
        for n in range(1):
            execution.execute_directory(path, config)

        os.remove(os.path.join('temp', 'execution.txt'))
