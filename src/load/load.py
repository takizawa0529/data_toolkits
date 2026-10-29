import sys

from src.load._to_s3 import ToS3
from src.utils import utils
from ._to_s3_injector import ToFileExecutor, ToFileInjector
import src.data_processing_toolkit as dpt
from src.data_processing_toolkit.data_processing_toolkit.utils.utils import parse_yaml

logger = utils.my_logger(__name__)

LOGFILE = './logs/app.log'
CONNECTION_CONFIG = './config/s3_connection.yaml'
LOAD_CONFIG = './config/load.yaml'

def main():
    logger.info('START: loading data.')

    dpt.set_verbose_logger()
    dpt.set_file_logger(LOGFILE)

    connection_info = parse_yaml(CONNECTION_CONFIG)
    data_copier = ToS3(**connection_info)

    injector = ToFileInjector(data_copier, LOAD_CONFIG)
    executor = ToFileExecutor(injector, skip_errors=True)
    n_errors = executor.execute()

    if n_errors > 0:
        logger.info(f'Total number of errors: {n_errors}')

    logger.info('DONE: loading data.')

    if n_errors > 0:
        sys.exit(1)

if __name__ == '__main__':
    main()

