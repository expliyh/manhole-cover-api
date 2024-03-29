import asyncio
import datetime

from fastapi import UploadFile

import config
from defines import PictureStatus, AuditStatus
from models import Cover, picture_registry, cover_registry
from models.engine import engine


async def add_cover(pid: int, file: bytes, status: str) -> int:
    cover = Cover()
    cover.picture_id = pid
    cover.status = status
    picture = await picture_registry.get_picture(pid)
    cover.latitude = picture.latitude
    cover.longitude = picture.longitude
    cover.positionFormat = picture.position_format
    cover.auditStatus = AuditStatus.NOT_VIEWED
    cover.recognizeResult = status
    cover.uploadTime = picture.uploadTime
    cover.uploadUser = picture.upload_user
    cover.url = None
    cover.recognizeTime = datetime.datetime.now()
    cover.editCount = 0
    cover.url = None

    cid = await engine.add(cover)

    with open(f'{config.file_path}cover_{cid}.webp', 'wb') as f:
        f.write(file)

    await cover_registry.update_url(cid, f'cover_{cid}.webp')
    return cid


async def fake_recognize(pid: int, file: bytes):
    await asyncio.sleep(5)
    cid = await add_cover(pid, file, "井盖完好")
    await picture_registry.update_status(pid, PictureStatus.RECOGNIZED)
