import pandas as pd
import pyathena
import warnings

from .config import settings
from ._datalake_sql_exeutor import DataLakeSqlExecutor

class DataLakeSqlExecutorRead(DataLakeSqlExecutor):
    def fetch(self, query: str) -> pd.DataFrame:
        with self._connection as connection:
            return pd.read_sql(query, connection)

    def _create_connection(self):
        self._connection = pyathena.connect(
            s3_staging_dir = settings.S3_STAGING_DIR,
            region_name = settings.REGION,
            work_group = settings.WORK_GROUP,
        )