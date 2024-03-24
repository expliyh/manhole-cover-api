from fastapi import HTTPException

from defines import PictureStatus
from models import picture_registry, cover_registry

from request_models import CoverInfo


async def get_cover(cid: int):
    cover = await cover_registry.get_cover(cid)
    if cover is None:
        raise HTTPException(status_code=404, detail="Cover not found")

    c_info: CoverInfo = CoverInfo()
    c_info.cid = cover.id
    c_info.pid = cover.picture_id
    c_info.url = cover.url
    c_info.uploadTime = cover.uploadTime
    c_info.recognizeTime = cover.recognizeTime
    c_info.uploadUser = cover.uploadUser
    c_info.status = cover.status
    c_info.auditStatus = cover.auditStatus
    c_info.recognizeResult = cover.recognizeResult
    c_info.correctedResult = cover.correctedResult
    c_info.latitude = cover.latitude
    c_info.longitude = cover.longitude
    c_info.positionFormat = cover.positionFormat

    return c_info
