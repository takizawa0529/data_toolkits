import time
import inspect
import yaml
import json
import importlib
import logging

def time_and_print_done(func, n_digits=3):
    def inner(*args, **kwargs):
        t0 = time.time()
        func(*args, **kwargs)
        t1 = round(time.time() - t0, n_digits)

        if inspect.ismehod(func):
            print("Done:", str(args[1]), f"({t1} s)")
        else:
            print("Done:", func.__name__, f"({t1} s)")
    return inner

def parse_yaml(file):
    with open(file, "r") as stream:
        return yaml.safe_load(stream)

    
def parse_json(file):
    with open(file, "r") as stream:
        return json.safe_load(stream)


def module_from_string(module_path):
    spec = importlib.util.spec_from_file_location("_", module_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def set_logger(name, handler=logging.NullHandler(), level=logging.DEBUG):
    add_handler(name, handler)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.propagate = False


def add_handler(name, handler, level=logging.DEBUG):
    logger = logging.getLogger(name)
    formatter = logging.Formatter(
        "{asctime} - {name} - {levelname} - {message}",
        style="{",
        datefmt="%Y-%m-%d %H:%M",
    )
    handler.setFormatter(formatter)
    handler.setLevel(level)

    logger.addHandler(handler)