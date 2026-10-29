import pandas as pd

from src.utils import utils
from src.data_processing_toolkit.data_processing_toolkit.dependency_injector import (
    DependencyInjector, InjectorExecutor
)

logger = utils.my_logger(__name__)

class ToFileInjector(InjectorExecutor):
    def __init__(self, *args, logger=logger, **kwargs):
        super().__init__(*args, logger=logger, **kwargs)


class ToFileExecutor(DependencyInjector):
    def __init__(self, data_copier, *args, **kwargs):
        self.data_copier = data_copier
        super().__init__(*args, **kwargs)

    def _parse_config_item(self, table, bundle):
        def output_callable():
            self._fix_dtypes(
                bundle['file_path'],
                bundle.get('output_dtypes', {})
            )

            self._data_copier.upload_file(
                bundle['file_path'],
                bundle['target_table']
            )

        output_callable.__name__ = table
        output_callable.__str__ = table
        self._output_list.append(output_callable)

    @staticmethod
    def _fix_dtypes(file_path, dtype_mapping):
        if not dtype_mapping:
            return

        df = pd.read_parquet(file_path)

        for col, dtype in dtype_mapping.items():
            if col not in df.columns:
                continue

            if dtype.lower() == 'decimal(12, 0)':
                df[col] = (
                    pd.to_numeric(
                        df[col],
                        errors = 'coerce'
                    )
                    .astype('Int64')
                )

        df.to_parquet(
            file_path,
            index=False
        )