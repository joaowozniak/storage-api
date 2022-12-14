from botocore.client import BaseClient
from dotenv import load_dotenv

import boto3
import os

load_dotenv("src/resources/.env")


class S3Config:
    """
    Handles AWS S3 configuration process and credentials variables
    """
    AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY")
    AWS_REGION = os.environ.get("AWS_REGION")
    AWS_S3_BUCKET = os.environ.get("AWS_S3_BUCKET")

    def get_base_client(self) -> BaseClient:
        """
        Generate an S3 Base Client instance in order to communicate with file storage space.
        :return: S3 Base Client
        """
        return boto3.client(
            service_name="s3",
            aws_access_key_id=self.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=self.AWS_SECRET_ACCESS_KEY,
        )
