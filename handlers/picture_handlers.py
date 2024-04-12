import datetime
import logging
import os
from typing import Annotated

from fastapi import UploadFile, APIRouter, HTTPException, File, Form, Header
import decimal

from models import user_registry
from services import upload_picture, get_picture

from request_models.UploadPictureRequest import UploadPictureRequest

import config

router = APIRouter()

logger = logging.getLogger(__name__)


@router.post("/api/picture/add")
async def upload_picture_handler(
        latitude: str = Form(),
        longitude: str = Form(),
        position_format: str = Form(),
        picture: UploadFile = File(),
        token: Annotated[str | None, Header()] = None
):
    if token is None:
        raise HTTPException(status_code=401, detail="请登录")
    user = await user_registry.get_user_by_access_token(token)
    if user is None:
        raise HTTPException(status_code=401, detail="登录失效，请重试")
    if "ADMIN" not in user.groups and "UPLOADER" not in user.groups:
        raise HTTPException(status_code=403, detail="权限不足")
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
    logger.info("New picture uploaded by user %s" % user.id)
    return await upload_picture(
        latitude=lat,
        longitude=lon,
        position_format=position_format,
        picture=picture,
        uid=user.id
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
