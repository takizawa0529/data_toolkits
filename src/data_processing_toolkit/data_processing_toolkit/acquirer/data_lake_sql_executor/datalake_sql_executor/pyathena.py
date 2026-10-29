import boto3
import pyathena
import pandas as pd

from pyathena.pandas.async_cursor import AsyncPandasCursor

from ._datalake_sql_executor import DatalakeSqlExecutor
from .config import settings
from ._exception import QueryExecutionError

class DatalakeSqlExceuterPyathena(DatalakeSqlExecuter):
    def __init__(self, n_workers=10):
        self._n_workers = n_workers
        self._athena_client = boto3.client("athena", settings.REGION)
        super().__init__()


    def fetch(self, query: str) -> pd.DataFrame:
        with self._connection as connection:
            query_id, future = connection.cursor(max_workers=self._n_workers).execute(query)
            result = future.result().as_pandas()
        status = self._athena_client.get_query_execution(QueryExecutionId=query_id)["QueryExecution"]["Status"]
        if status["State"] == "FAILED":
            raise QueryExecutionError(status.get("StateChangeReason", "No reason provided."))
        return result

    def _create_connection(self):
        self._connection = pyathena.connect(
            s3_staging_dir=settings.S3_STAGING_DIR,
            region_name=settings.REGION,
            work_group=settings.WORK_GROUP,
            cursor_class=AsyncPandasCursor,
        )