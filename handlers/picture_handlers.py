import datetime
import os

from fastapi import UploadFile, APIRouter, HTTPException, File, Form
import decimal

from services import upload_picture, get_picture

from request_models.UploadPictureRequest import UploadPictureRequest

import config

router = APIRouter()


@router.post("/api+"
             "")
async def upload_picture_handler(
        latitude: str = Form(),
        longitude: str = Form(),
        position_format: str = Form(),
        picture: UploadFile = File()
):
    lat = decimal.Decimal(latitude)
    lon = decimal.Decimal(longitude)
    if lon > 180 or lon < -180:
        raise HTTPException(status_code=400, detail="Invalid longitude")
    if lat > 90 or lat < -90:
        raise HTTPException(status_code=400, detail="Invalid latitude")
    # TODO: 检查 position_format 是否合法
    ext = os.path.splitext(picture.filename)[-1][1:]
    if ext not in config.allow_picture_exts:
        raise HTTPException(status_code=415, detail=f"Invalid file type {ext}")
    return await upload_picture(
        latitude=lat,
        longitude=lon,
        position_format=position_format,
        picture=picture
    )


@router.get("/api/picture/get")
async def get_picture_handler(
        pid: int
):
    if pid == -1:
        return {
            "pid": -1,
            "pictureLink": 'picture.url',
            "uploadTime": datetime.datetime.now(),
            "recognizeTime": datetime.datetime.now(),
            "uploadUser": -1,
            "status": 'UPLOADED',
            "result": '识别中'
        }
    return await get_picture(pid)
    pass
