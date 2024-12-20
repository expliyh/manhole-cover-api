from fastapi import APIRouter
from fastapi.responses import FileResponse

from services import file_service

file_router = APIRouter()


@file_router.get('/api/file/get')
async def get_file_query(filename: str):
    return FileResponse(file_service.getter.get_path(filename))


@file_router.get('/api/file/{filename}')
async def get_file_path(filename: str):
    return FileResponse(file_service.getter.get_path(filename))


@file_router.get('/api/download/{filename}')
async def download(filename: str):
    path, name = file_service.getter.get_path_and_name(filename)
    return FileResponse(
        path,
        headers={
            "Content-Disposition": "attachment; filename={}".format(name)
        })
