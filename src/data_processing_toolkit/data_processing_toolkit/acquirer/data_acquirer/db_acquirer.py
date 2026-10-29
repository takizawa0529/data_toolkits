import pandas as pd

from ._base import BaseAcquirer, BaseDataFactory
from .. import data_lake_sql_executor

class DbDataFactory(BaseDataFactory):
    def _create_acquirer(self, query, keep_empty_str=False):
        return ReadsqlAcquirer(query) if keep_empty_str else PyathenaAcquirer(query)

def PyathenaAcquirer(BaseAcquirer):
    def __init__(self, query):
        self.query = query
        self.acquirer = data_lake_sql_executor.DataLakeSqlExecuterPyathena()

    def acquire(self):
        return self.acquirer.fetch(self.query)


def ReadsqlAcquirer(BaseAcquirer):
    def __init__(self, query):
        self.query = query
        self.acquirer = data_lake_sql_executor.DataLakeSqlExecutorReadSql()

    def acquire(self):
        return self.acquirer.fetch(self.query)