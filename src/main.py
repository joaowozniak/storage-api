from typing import List
from fastapi import FastAPI, UploadFile, status, Header, Depends
from src.services.storage_service import StorageService
from src.security.security_service import SecurityService

app = FastAPI(
    title="storage-api",
    description="Use storage-api to store, retrieve or delete files",
)

service = StorageService()
security = SecurityService()


@app.post(
    "/upload",
    status_code=status.HTTP_201_CREATED,
    summary="Upload files",
    description="Upload valid for pdf or image files",
    name="POST files to Storage-Api",
    response_description="File upload OK",
)
async def upload_file(
        file: UploadFile,
        path: str = Header(default=None),
        addinfo: List[str] = Header(default=None),
        username: str = Depends(security.validate_user)):
    return service.upload_file(file, path, addinfo, username)


@app.get(
    "/download",
    status_code=status.HTTP_200_OK,
    summary="Download files",
    description="Download previously uploaded files",
    name="GET files from Storage-Api",
    response_description="File download OK",
)
async def download_file(path: str, username: str = Depends(security.validate_user)):
    return service.download_file(path, username)


@app.delete(
    "/delete",
    status_code=status.HTTP_200_OK,
    summary="Delete files",
    description="Delete previously uploaded files",
    name="DELETE files from Storage-Api",
    response_description="File deleted OK",
)
async def delete(path: str, username: str = Depends(security.validate_user)):
    return service.delete_file(path, username)
