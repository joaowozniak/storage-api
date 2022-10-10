import logging


class PathService:
    """
    Handles S3 paths generation
    """

    @staticmethod
    def get_file_path(filename, path) -> str:
        """
        Calculates the S3 path in which file will be stored
        :param filename: Name of file to be stored
        :param path: User's desired storing path
        :return: S3 path
        """
        logging.log(level=20, msg="Calculating S3 path...")
        if path:
            if path[-1] == "/":
                path = path[:-1]
            if path[0] == "/":
                path = path[1:]

            s3_path = path + "/" + filename
        else:
            s3_path = filename

        return s3_path
