import boto3
import time
import logging
import pandas as pd

from ._datalake_sql_executor import DatalakeSqlExecuter
from .config import settings
from ._exceptions import QueryExecutionError

logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.DEBUG)
logger.propagate = False


class DatalakeSqlExecutorBoto3(DatalakeSqlExecuter):
    def _create_connection(self) -> None:
        self._athena_client = boto3.client("athena", region_name=settings.REGION)


    def fetch(self, query: str, **kwargs) -> pd.DataFrame:
        s3_path = self._query(query)
        return pd.read_csv(s3_path, **kwargs)


    def download(self, query: str, csv_path: str) -> None:
        s3_path = self._query(query)
        exclude_prefix = "s3://"
        bucket_name, s3_file_path = s3_path[len(exclude_prefix):].split(
            "/", maxsplit=1
        )
        s3 = boto3.client("s3")
        s3.download_file(bucket_name, s3_file_path, csv_path)


    def _query(self, query: str):
        athena_exec_id = self._kick_query(query)
        return self._check_query_completion(athena_exec_id)


    def _kick_query(self, query: str):
        query_exec_js = self._athena_client.start_query_execution(
            QueryString=query, WorkGroup=settings.WORK_GROUP
        )
        athena_exec_id = query_exec_js["QueryExecutionId"]
        logger.debug(f"Query execution ID: {athena_exec_id}")
        return athena_exec_id

    
    def _check_query_completion(self, athena_exec_id: str) -> str:
        state = "UNEXECUTED"
        while state not in ("SUCCEEDED", "FAILED"):
            status = self._athena_client.get_query_execution(
                QueryExecutionId = athena_exec_id
            )["QueryExecution"]["Status"]
            logger.debug(state)
            time.sleep(settings.SLEEP_TIME_SEC)

        if state == "FAILED":
            logger.error("query failed")
            raise QueryExecutionError(
                status.get("StateChangeReason", "No reason provided.")
            )
        s3_path = self._athena_client.get_query_execution(
            QueryExecutionId = athena_exec_id
        )["QueryExecution"]["ResultConfiguration"]["OutputLocation"]

        logger.debug("query succeeded!\n")
        logger.debug(f"csv saved to:\n{s3_path}")
        return s3_path
