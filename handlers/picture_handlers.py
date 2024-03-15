import os

from fastapi import UploadFile, APIRouter, HTTPException
import decimal

from services import upload_picture

import config

router = APIRouter()


@router.post("/api/picture/add")
async def upload_picture_handler(
        latitude: str,
        longitude: str,
        position_format: str,
        picture: UploadFile
):
    lat = decimal.Decimal(latitude)
    lon = decimal.Decimal(longitude)
    if lon > 180 or lon < -180:
        raise HTTPException(status_code=400, detail="Invalid longitude")
    if lat > 90 or lat < -90:
        raise HTTPException(status_code=400, detail="Invalid latitude")
    # TODO: 检查 position_format 是否合法
    ext = os.path.splitext(picture.filename)[-1]
    if ext not in config.allow_picture_exts:
        raise HTTPException(status_code=415, detail="Invalid file type")
    return await upload_picture(
        latitude=lat,
        longitude=lon,
        position_format=position_format,
        picture=picture
    )
