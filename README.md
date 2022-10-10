# Storage-api

Storage-api allows users to store files in the cloud through a simple-to-use API.

## Getting started

In order to use the api locally, git clone this project and simply hit:

```shell
docker-compose up
```

The code above creates and starts the container image. Once finished, the api is ready to use.

## Functional features

This project is a minimal HTTP based API that allows the users to do the following:

* Upload a file. User is able to attach one key-value metadata pair per file and to specify the saving path.
* Download a previously uploaded file. It also retrieves any file metadata if exists.
* Delete a previously uploaded file.

## Security

This api uses basic auth.

## Endpoints

Available endpoints and examples:

* POST /upload
    * Body (form-data) -> file: path to file to upload
    * Headers:
        * File metadata Key (order matters) -> addinfo: KEY
        * File metadata Value -> addinfo: VALUE
        * Saving path: path -> "saving/path/"

    * Returns: Saving reference

```shell
curl --location --request POST 'host:port/upload' \
--header 'addinfo: KEY' \
--header 'addinfo: VALUE' \
--header 'path: saving/path/' \
--header 'Authorization: Basic ENCONDED_CREDENTIALS' \
--form 'file=@"path/to/file/to/upload/in/local/filesys/filename.extension"'
```

* GET /download
    * Query params -> path: Saving reference

    * Returns: Presigned url to download file and file metadata.

```shell
curl --location --request GET 'host:port/download?path=saving/reference/filename.extension' \
--header 'Authorization: Basic ENCONDED_CREDENTIALS'
```

* DELETE /delete
    * Query params -> path: Saving reference

    * Returns: Deletion status

```shell
curl --location --request DELETE 'host:port/download?path=saving/reference/filename.extension' \
--header 'Authorization: Basic ENCONDED_CREDENTIALS'
```





