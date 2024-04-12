import asyncio
import datetime
import os.path
import threading

import numpy as np

import config
import decimal
from fastapi import UploadFile
import cv2 as cv2

from defines import PictureStatus
from models import Picture, picture_registry
from recognize import yolo
from recognize.test3 import filter_box, get_result
from .add_cover import add_cover

detect_tasks = set()


async def det(pid: int, file: bytes):
    img = cv2.imdecode(np.frombuffer(file, np.uint8), cv2.IMREAD_COLOR)

    _, result = yolo.run(img)

    img1 = cv2.imdecode(np.frombuffer(file, np.uint8), cv2.IMREAD_COLOR)
    height, width = img1.shape[:2]
    # y_rito = height / 640
    # x_rito = width / 640
    y_rito = 1
    x_rito = 1

    # outbox = filter_box(output, 0.5, 0.5)  # 最终剩下的Anchors：0 1 2 3 4 5 分别是 x1 y1 x2 y2 score class
    #
    # result = get_result(outbox)

    for i in result:
        top, left, right, bottom = i[2]
        c_img = img1.copy()
        cv2.rectangle(c_img, (int(top * x_rito), int(left * y_rito), int(right * x_rito), int(bottom * y_rito)),
                      (255, 0, 0), 10)
        result, encoded_image = cv2.imencode('.webp', c_img)
        await add_cover(pid, encoded_image.tobytes(), i[0], i[1])

        await picture_registry.update_status(pid, PictureStatus.RECOGNIZED)


async def upload_picture(
        latitude: decimal.Decimal,
        longitude: decimal.Decimal,
        position_format: str,
        picture: UploadFile,
        uid: int
):
    picture_info = Picture()
    picture_info.latitude = latitude
    picture_info.longitude = longitude
    picture_info.position_format = position_format
    picture_info.url = None
    picture_info.uploadTime = datetime.datetime.now()
    picture_info.upload_user = uid
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
