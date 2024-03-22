from fastapi import HTTPException

from defines import PictureStatus
from models import picture_registry, cover_registry


async def get_picture(pid: int):
    picture = await picture_registry.get_picture(pid)
    if picture is None:
        raise HTTPException(status_code=404, detail="Picture not found")
    if picture.status == PictureStatus.UPLOADED:
        result = '识别中'
    elif picture.status == PictureStatus.RECOGNIZED:
        cover_list = await cover_registry.list_covers_by_pid(pid)
        have_bad = False
        for i in cover_list:
            if i.recognizeResult != '井盖完好':
                have_bad = True
                break
        if have_bad:
            result = '存在问题'
        else:
            result = '井盖完好'
    else:
        result = '未知'

    return {
        "pid": picture.id,
        "pictureLink": picture.url,
        "uploadTime": picture.uploadTime,
        "recognizeTime": picture.recognizeTime,
        "uploadUser": uid if (uid := picture.upload_user) is not None else "-1",
        "status": picture.status,
        "result": result
    }
    pass
