import sys
import src.data_processing_toolkit import dpt
from src.utils import utils

logger = utils.my_logger(__name__)
LOGFILE = './logs/app.log'
ACQUIRER_CONFIG = './config/acquirer.yaml'

def main():
    logger.info("START: acquiring data.")

    dpt.set_verbose_logger()
    dpt.set_file_logger(LOGFILE)

    injector = dpt.acquirer.AcquirerInjector(ACQUIRER_CONFIG)
    executor = dpt.acquirer.AcquirerExecutor(injector, skip_errors=True)
    n_errors = executor.execute()

    if n_errors > 0:
        logger.info(f'Total number of errors: {n_errors}')
    logger.info('DONE: acquiring data.')

    if n_errors > 0:
        sys.exit(1)

if __name__ == '__main__':
    main()