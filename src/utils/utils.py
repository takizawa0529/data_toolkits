import logging

from ..data_processing_toolkit.data_processing_toolkit.utils.utils import set_logger, add_handler

def my_logger(name, file_path="./logs/app.log"):
    set_logger(name, handler=logging.StrwamHandler())
    add_handler(name, handler=logging.FileHandler(file_path))
    return logging.getLogger(name)