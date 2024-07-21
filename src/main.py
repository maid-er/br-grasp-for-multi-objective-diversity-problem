'''Main function'''
import os

from utils import execution
from utils.config import read_config
from utils.logger import load_logger

logging = load_logger(__name__)

config = read_config('config')


if __name__ == '__main__':
    logging.info('Initializing diversity maximization algorithm...')

    path = os.path.join('instances', 'GDP')

    # execution.execute_instance(path, config)
    execution.execute_directory(path, config)
