import logging

from ._executor_factory import MonolithicQueryExecutorFactory, CompositeQueryExecutorFactory, FileExecutorFactory
from ..dependency_injector import DependencyInjector, InjectorExecutor

logger = logging.getLogger(__name__)

class AcquireExecutor(InjectorExecutor):
    def __init__(self, *args, logger=logger, **kwargs):
        super().__init__(*args, logger=logger, **kwargs)


class AcquireInjector(DependencyInjector):
    _FORMATS = {
        "columns": {
            "fields": ("columns", "rest_of_query", "raw_file_path"),
            "obj": CompositeQueryExecutorFactory,
        },
        "query": {
            "fields": ("query", "raw_file_path"),
            "obj": MonolithicQueryExecutorFactory,
        },
        "file": {
            "fields": ("input_file_path", "raw_file_path"),
            "obj": FileExecutorFactory,
        },
    }
    _COMMON_ARGS = ["raw_file_path"]
    _OPTIONAL_ARGS = ["keep_empty_str"]

    def _parse_config_item(self, table, bundle):
        relevant_fields = self._filter_irrelevant_fields(bundle.keys())
        factory = self._simple_factory(relevant_fields)

        args = {key: val for key, val in bundle.items() if key in relevant_fields}
        pargs = [args.pop(pos_arg) for pos_arg in self.__class__.COMMON_ARGS]
        kwargs = args

        def output_callable():
            factory().get_and_save_data(*pargs, **kwargs)

        output_callable.__name__ = table
        output_callable.__str__ = table


    @classmethod
    def _filter_irrelevant_fields(cls, fields):
        possible_fields = set(cls._OPTIONAL_ARGS)
        for bundle in cls._FORMATS.values():
            possible_fields |= set(bundle["fields"])
        return set(fields) & possible_fields


    @classmethod
    def _simple_factory(cls, fields):
        for format_bundle in cls._FORMATS.values():
            if not set(format_bundle["fields"]) - set(fields):
                return format_bundle["obj"]
        logger.error("Config does not match any of the expected formats.")
        raise ValueError("Config does not match any of the expected formats.")