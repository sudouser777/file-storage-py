import logging
from pathlib import Path
from typing import Any

import boto3
from boto3_type_annotations.s3 import Client

from ..common_util import read_config_yaml
from ..file_system import BaseFileSystem

logger = logging.getLogger(__name__)


# noinspection PyMethodMayBeStatic
class S3FileSystem(BaseFileSystem):
    name = 'aws_s3'

    def __init__(self) -> None:
        self.config = read_config_yaml(self.name)

    def create_client(self) -> Client:
        s3: Client = boto3.client(
            's3',
            region_name=self.config['region_name'],
            aws_access_key_id=self.config['access_key_id'],
            aws_secret_access_key=self.config['secret_access_key']
        )
        return s3

    def upload_callback(self, nbytes: int):
        logger.debug(f'File uploaded successfully. Number of bytes: {nbytes}')

    def upload_file(self, file: str | Path, **kwargs: Any) -> None:
        s3 = self.create_client()
        try:
            bucket = kwargs.get('bucket', self.config.get('bucket'))
            key = kwargs.get('key')
            if not all((bucket, key)):
                raise Exception()
            s3.upload_file(
                Bucket=bucket,
                Filename=str(file),
                Key=key,
                Callback=self.upload_callback
            )
        finally:
            s3.close()

    def download_callback(self, nbytes: int):
        logger.debug(f'File downloaded successfully. Number of bytes: {nbytes}')

    def download_file(self, file: str | Path, destination: str | Path, **kwargs) -> None:
        s3 = self.create_client()
        try:
            bucket = kwargs.get('bucket', self.config.get('bucket'))
            key = kwargs.get('key')
            if not all((bucket, key)):
                raise Exception()
            s3.download_file(
                Bucket=bucket,
                Filename=str(file),
                Key=key,
                Callback=self.download_callback
            )
        finally:
            s3.close()

    def delete_file(self, file: str | Path, **kwargs: Any) -> None:
        s3 = self.create_client()
        try:
            bucket = kwargs.get('bucket', self.config.get('bucket'))
            key = kwargs.get('key')
            if not all((bucket, key)):
                raise Exception()
            s3.delete_object(
                Bucket=bucket,
                Key=key
            )
            logger.debug('File deleted successfully')
        finally:
            s3.close()
