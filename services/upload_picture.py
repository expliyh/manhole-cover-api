import asyncio
import datetime
import os.path
import threading

import config
import decimal
from fastapi import UploadFile

from defines import PictureStatus
from models import Picture, picture_registry
from recognize import yolo
from recognize.test3 import filter_box, draw
from .add_cover import fake_recognize, add_cover

detect_tasks = set()


async def det(pid: int, file: bytes):
    output, or_img = yolo.inference(img_file=file)

    outbox = filter_box(output, 0.5, 0.5)  # 最终剩下的Anchors：0 1 2 3 4 5 分别是 x1 y1 x2 y2 score class

    result, or_img = draw(or_img, outbox)

    for i in result:
        await add_cover(pid, or_img, i[0])

    await picture_registry.update_status(pid, PictureStatus.RECOGNIZED)


async def upload_picture(
        latitude: decimal.Decimal,
        longitude: decimal.Decimal,
        position_format: str,
        picture: UploadFile
):
    picture_info = Picture()
    picture_info.latitude = latitude
    picture_info.longitude = longitude
    picture_info.position_format = position_format
    picture_info.url = None
    picture_info.uploadTime = datetime.datetime.now()
    picture_info.upload_user = None
    pid = await picture_registry.add_picture(picture_info)
    origin_name = picture.filename
    origin_ext = os.path.splitext(origin_name)[-1]
    filename = f'pic_{pid}{origin_ext}'
    pic_file = await picture.read()
    with open(f'{config.file_path}{filename}', 'wb+') as f:
        f.write(pic_file)
    await picture_registry.update_url(pid, filename)

    task = asyncio.create_task(det(pid, pic_file))
    detect_tasks.add(task)
    task.add_done_callback(detect_tasks.discard)
    # threading.Thread(target=det, args=(pid, pic_file)).run()
    # await det(pid, pic_file)

    # await task

    return {
        'status': 'success',
        'pid': pid,
        'message': 'Picture uploaded successfully'
    }
