import sys

from src.utils import utils
import src.data_processing_toolkit import dpt
from .preprocess_executor import PreprocessExecutor, PreprocessInjector


logger = utils.my_logger(__name__)

LOGFILE = './logs/app.log'
PREPROCESS_CONFIG = './config/preprocess.yaml'

def main():
    logger.info("START: preprocessing data.")

    dpt.set_verbose_logger()
    dpt.set_file_logger(LOGFILE)

    injector = PreprocessInjector(PREPROCESS_CONFIG)
    executor = PreprocessExecutor(injector, skip_errors=True)
    n_errors = executor.execute()

    if n_errors > 0:
        logger.info(f'Total number of errors: {n_errors}')
    logger.info('DONE: preprocessing data.')

    if n_errors > 0:
        sys.exit(1)

if __name__ == '__main__':
    main()