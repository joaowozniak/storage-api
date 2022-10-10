import logging

from typing import List
from fastapi import UploadFile, HTTPException, status
from fastapi.responses import JSONResponse
from src.config.s3_config import S3Config
from src.services.path_service import PathService


class StorageService:
    """
    Handles basic functions to communicate with S3: upload, download, delete
    """
    s3_config = S3Config()
    path_service = PathService()

    def upload_file(
            self, file: UploadFile, path: str, addinfo: List[str], username: str
    ) -> JSONResponse:
        """
        Uploads file to S3
        :param file: File to be uploaded
        :param path: S3 path in whichi file will be stored
        :param addinfo: [Optional] Key-value style tags to the document upload
        :param username: Logged-in username
        :return: S3 path that should be used to retrieve document
        """

        s3_client = self.s3_config.get_base_client()

        s3_path = self.path_service.get_file_path(file.filename, path)
        s3_key = f"{username}/" + s3_path

        logging.log(level=20, msg=f"Uploading file to path: {s3_path}")

        metadata = self.__get_file_metadata(addinfo)

        upload_response = s3_client.put_object(
            Body=file.file.read(), Bucket=S3Config.AWS_S3_BUCKET, Key=s3_key
        )

        if upload_response:
            # add key-value tag when file successfully uploaded
            if metadata is not None:
                s3_client.put_object_tagging(
                    Bucket=S3Config.AWS_S3_BUCKET, Key=s3_key, Tagging=metadata
                )

            return JSONResponse(
                content=f"File upload OK. Use path reference to retrieve your file: {s3_path}",
                status_code=status.HTTP_201_CREATED,
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="FAILED: File upload KO",
            )

    @staticmethod
    def __get_file_metadata(addinfo: List[str]):
        if addinfo and len(addinfo) >= 2:
            if addinfo[0] and addinfo[1]:
                return {"TagSet": [{"Key": addinfo[0], "Value": addinfo[1]}]}
        return None

    def download_file(self, path: str, username: str):
        """
        Generates an S3 presigned url that can be used to download file
        :param path: S3 path including filename in which file is stored
        :param username: Logged-in username
        :return: S3 Presigned url of file and additional information saved as tags
        """

        s3_client = self.s3_config.get_base_client()

        logging.log(level=20, msg=f"Downloading file from path: {path}")

        prefix = f"{username}/" + path
        obj_list = self.__check_if_exists(s3_client, prefix)

        presigned_url = s3_client.generate_presigned_url(
            ClientMethod="get_object",
            Params={
                "Bucket": S3Config.AWS_S3_BUCKET,
                "Key": obj_list["Contents"][0]["Key"],
            },
            ExpiresIn=300,
        )

        tags = s3_client.get_object_tagging(Bucket=S3Config.AWS_S3_BUCKET, Key=prefix)

        if not presigned_url:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="FAILED: Download URL could not be generated",
            )

        return {"Download your file here": presigned_url, "Tags": tags["TagSet"]}

    def delete_file(self, path: str, username: str) -> JSONResponse:
        """
        Deletes previously uploaded file from S3 storage
        :param path: S3 path of file to be deleted
        :param username: Logged-in username
        :return: Path of deleted file
        """
        s3_client = self.s3_config.get_base_client()

        logging.log(level=20, msg=f"Deleting file from path: {path}")

        prefix = f"{username}/" + path
        obj_list = self.__check_if_exists(s3_client, prefix)

        delete_response = s3_client.delete_object(
            Bucket=S3Config.AWS_S3_BUCKET, Key=obj_list["Contents"][0]["Key"]
        )

        if delete_response:
            return JSONResponse(
                content=f"File deleted from path: {path}",
                status_code=status.HTTP_200_OK,
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="FAILED: File delete KO",
            )

    @staticmethod
    def __check_if_exists(s3_client, prefix) -> list:

        obj_list = s3_client.list_objects(Bucket=S3Config.AWS_S3_BUCKET, Prefix=prefix)

        if "Contents" not in obj_list:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="FAILED: File specified in path not found",
            )

        return obj_list
