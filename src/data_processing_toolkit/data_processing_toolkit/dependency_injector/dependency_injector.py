from abc import ABC, abstractmethod
import logging

from ..utils import utils

LOGGER = logging.getLogger(__name__)

class InjectorExecutor:
    def __init__(self, injector_iterator, skip_errors=False, logger=None):
        self._injector_iterator = injector_iterator
        self._skip_errors = skip_errors
        self._logger = LOGGER if logger is None else logger


    def execute(self):
        try:
            self._setup()
            return self._execute()        
        except Exception as e:
            self._logger.error(
                f'Exception raised inside _setup() or _execute():\n{e}\nwill abort and proceed to _teardown()'
            )  
            raise
        finally:
            self._teardown()


    def _setup(self):
        self._injector_iterator.setup()


    def _execute(self):
        n_errors = 0
        for item in self._injector.generate_iterator():
            self._logger.info(f"Execute: {item.__name__}")
            try:
                item()
            except KeyboardInterrupt:
                raise
            except Exception as e:
                n_errors += 1
                self._logger.error(f"Runtime error raised for {item.__name__}:\n{e}")
                if not self._skip_errors:
                    raise e
                self._logger.warning(f"Error raised for {item.__name__}, but will pass since skip_errors=True.")
        return n_errors


    def _teardown(self):
        self._injector_iterator().teardown()


class DependencyInjector(ABC):
    def __init__(self, config_path, module_paths=None):
        self._config_path = config_path
        self._module_paths = [] if module_paths is None else module_paths
        self._modules = []
        self._output_list = []


    def generate_iterator(self):
        for module_path in self._module_paths:
            self._modules.append(utils.module_from_string(module_path))

        config = utils.parse_yaml(self._config_path)

        for header, bundle in config.items():
            self._parse_config_item(header, bundle)

        return iter(self._output_list)


    @abstractmethod
    def _parse_config_item(self, header, bundle):
        pass


    def _get_object_from_module(self, object_name, parent_object=object):
        target_object = None
        for module in self._modules:
            if hasattr(module, object_name):
                target_object = getattr(module, object_name)
        if target_object is None:
            raise AttributeError("object not present in any of the provided modules.")
        if not issubclass(target_object, object):
            raise ValueError(f"object must inherit from {parent_object}.")
        return target_object


    def setup(self):
        pass


    def teardown(self):
        pass