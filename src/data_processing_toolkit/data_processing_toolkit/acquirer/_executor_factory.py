from abc import ABC, abstractmethod

import pandas as pd

from .data_acquirer.db_acquirer import DbDataFactory
from .data_acquirer.file_acquirer import FileDataFactory


# abstract creator
class ExecutorFactory(ABC):
    def get_and_save_data(self, out_file_path, **kwargs):
        executor = self._create_executor()
        df = executor.execute(**kwargs)
        df.to_parquet(out_file_path)

    @abstractmethod
    def _create_executor(self):
        pass


# concrete creators
class MonolithicQueryExecutorFactory(ExecutorFactory):
    def _create_executor(self):
        return MonolithicQueryExecutor()

class CompositeQueryExecutorFactory(ExecutorFactory):
    def _create_executor(self):
        return CompositeQueryExecutor()

class FileExecutorFactory(ExecutorFactory):
    def _create_executor(self):
        return FileExecutor()


# abstract product
class Executor(ABC):
    @abstractmethod
    def execute(self) -> pd.DataFrame:
        pass


# concrete products
class MonolithicQueryExecutor(Executor):
    def execute(self, query, keep_empty_str=False):
        return DbDataFactory().get_data(query=query, keep_empty_str=keep_empty_str)


class CompositeQueryExecutor(Executor):
    def execute(self, columns, rest_of_query, keep_empty_str=False):
        query = " ".join((
            "SELECT",
            ",".join(columns.keys()),
            rest_of_query,
        ))
        return DbDataFactory().get_data(query=query, keep_empty_str=keep_empty_str)


class FileExecutor(Executor):
    def execute(self, input_file_path, columns=None, read_kwargs=None):
        if columns is None:
            dtype = None
            usecols = None
        else:
            dtype = {col: bundle["dtype"] for col, bundle in columns.items()}
            usecols = list(columns.keys())

        if read_kwargs is None:
            read_kwargs = {}

        return FileDataFactory().get_data(
            file_path=input_file_path,
            usecols=usecols,
            dtype=dtype,
            **read_kwargs
        )


