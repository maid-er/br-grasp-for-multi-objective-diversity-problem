'''Main function'''
import os

from utils import execution
from utils.config import read_config
from utils.logger import load_logger

logging = load_logger(__name__)

config = read_config('config')


if __name__ == '__main__':
    logging.info('Initializing diversity maximization algorithm...')

    path = os.path.join('instances', 'GDP_test', 'GKD-c')

    # execution.execute_instance(path, config)
    for n in range(10):
        execution.execute_directory(path, config)

    os.remove(os.path.join('temp', 'execution.txt'))
