from abc import ABC, abstractmethod

import os
import subprocess

from . import _utils
from src.utils.utils import my_logger

logger = my_logger(__name__)

class ToS3:
    def __init__(self, bucket_path: str) -> None:
        if not bucket_path.endswith('/'):
            bucket_path += '/'
        self._bucket_path = bucket_path

    def upload_file(self, local_path: str, upload_path: str) -> str:
        if not os.path.exists(local_path):
            logger.error(f'ファイル不存在：{local_path}')
            raise FileNotFoundError(f"{local_path}が存在しません")

        s3_path = self._bucket_path + upload_path
        command = ["aws", "s3", "cp", local_path, s3_path]

        try:
            result = subprocess.run(
                command,
                capture_output = True,
                text = True,
                check = True
            )
            logger.info(f'Upload: {local_path} -> {s3_path}')
            logger.debug(result.stdout)

        except subprocess.CalledProcessError as e:
            logger.error("S3アップロード失敗")
            logger.error(e.stderr)
            raise RuntimeError("S3アップロードに失敗しました") from e