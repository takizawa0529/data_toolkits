import logging
import pandas as pd
from .preprocess.report import ReportProcessor
from src.data_processing_toolkit.data_processing_toolkit.dependency_injector import (
    DependencyInjector,
    InjectorExecutor
)

PROCESSORS = {"report": ReportProcessor,}
logger = logging.getLogger(__name__)

class PreprocessExecutor(InjectorExecutor):
    def __init__(self, *args, logger=logger, **kwargs):
        super().__init__(*args, logger=logger, **kwargs)

class PreprocessInjector(DependencyInjector):
    def _parse_config_item(self, table, bundle):
        read_file_paths = bundle['read_file_paths']
        processed_file_path = bundle['processed_file_path']

        def output_callable():
            dfs = {
                name: pd.read_parquet(path)
                for name, path in read_file_paths.items()
            }

            processor = PROCESSORS[table]()
            processed_df = processor.execute(dfs)
            processed_df.to_parquet(processed_file_path, index=False,)
        output_callable.__name__ = table
        output_callable.__str__ = table

        self._output_list.append(output_callable)