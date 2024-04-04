import json
import time
from datetime import datetime

from models import user_registry, cover_registry
from config import file_path
import token_utils


class ExportUserInfo:
    delete_time: str
    delete_stamp: int
    real_name: str
    uid: int
    username: str
    full_name: str
    email: str
    phone: str
    covers_upload: list[int]


async def generate_user_data(uid: int) -> str:
    user = await user_registry.get_user_by_id(uid)
    covers = await cover_registry.get_list_by_uid(uid)
    info = ExportUserInfo()
    info.delete_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    info.delete_stamp = int(time.time())
    info.uid = user.id
    info.username = user.username
    info.full_name = user.fullname
    info.email = user.email
    info.phone = user.phone
    info.real_name = f"userdata-{uid}.json"
    for i in covers:
        info.covers_upload.append(i.id)

    filename = f'{token_utils.generate_random_string(64)}.json'

    json.dump(info.__dict__, fp=open(f'{file_path}{filename}', mode='w+', encoding='utf-8'), ensure_ascii=False)

    return filename
