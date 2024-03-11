from fastapi import UploadFile
from models import Picture


async def upload_picture(
        latitude: int,
        longitude: int,
        position_format: str,
        picture: UploadFile
):
    picture_info = Picture()
    picture_info.latitude = latitude
    picture_info.longitude = longitude
    picture_info.position_format = position_format

