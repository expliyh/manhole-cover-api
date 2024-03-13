import os.path

import config

from fastapi import UploadFile
from models import Picture, picture_regiesry


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
    picture_info.url = None
    pid = await picture_regiesry.add_picture(picture_info)
    origin_name = picture.filename
    origin_ext = os.path.split(origin_name)[-1]
    filename = f'pic_{pid}.{origin_ext}'
    with open(f'{config.file_path}{filename}', 'wb') as f:
        f.write(await picture.read())
    await picture_regiesry.update_url(pid, filename)
