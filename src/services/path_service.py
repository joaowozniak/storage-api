import logging


class PathService:
    @staticmethod
    def get_file_path(filename, path):
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
