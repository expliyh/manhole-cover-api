from fastapi import HTTPException

from models import picture_registry


async def get_picture(pid: int):
    picture = await picture_registry.get_picture(pid)
    if picture is None:
        raise HTTPException(status_code=404, detail="Picture not found")
    return {
        "id": picture.id,
        "pictureLink": picture.url,
        "uploadTime": picture.uploadTime
    }
    pass
