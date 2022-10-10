import csv
import logging
import secrets

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials


class SecurityService:
    basic_auth = HTTPBasic()

    def validate_user(self, credentials: HTTPBasicCredentials = Depends(basic_auth)):
        logging.log(level=20, msg="Verifying user authentication...")
        current_username_bytes = credentials.username.encode("utf8")
        current_password_bytes = credentials.password.encode("utf8")

        if not self.__verify_user_in_db(current_username_bytes, current_password_bytes):
            logging.log(
                level=30, msg=f"Failed to validate user: {credentials.username}"
            )
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect credentials",
                headers={"WWW-Authenticate": "Basic"},
            )
        return credentials.username

    @staticmethod
    def __verify_user_in_db(
        current_username_bytes: bytes, current_password_bytes: bytes
    ):
        with open("src/resources/users.csv", "r") as file:
            csv_reader = csv.reader(file)
            next(csv_reader)  # skip header
            for row in csv_reader:
                user_db_bytes, pass_db_bytes = row[0].encode("utf8"), row[1].encode(
                    "utf8"
                )

                if secrets.compare_digest(
                    current_username_bytes, user_db_bytes
                ) and secrets.compare_digest(current_password_bytes, pass_db_bytes):
                    logging.log(level=20, msg="User verification OK")
                    return True

        return False
