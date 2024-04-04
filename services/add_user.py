import re

from fastapi import HTTPException

import request_models
from models import user_registry, User

import token_utils


async def add_user(req: request_models.AddUserRequest):
    if await user_registry.get_user_by_id(req.uid) is not None:
        raise HTTPException(status_code=400, detail="已存在 UID 相同的用户")
    if await user_registry.get_user_by_username(req.username) is not None:
        raise HTTPException(status_code=400, detail="已存在用户名相同的用户")
    if await user_registry.get_user_by_email(req.email) is not None:
        raise HTTPException(status_code=400, detail="已存在电子邮件地址相同的用户")
    if await user_registry.get_user_by_phone(req.phone) is not None:
        raise HTTPException(status_code=400, detail="已存在手机号码相同的用户")
    if len(req.password) < 8:
        raise HTTPException(status_code=404, detail="密码太短")
    if (not re.search(r"\d", req.password) or
            not re.search(r"[A-Z]", req.password) or
            not re.search(r"[a-z]", req.password)
    ):
        raise HTTPException(status_code=400, detail="密码过于简单，至少包含一个大写字母、一个小写字母和一个数字")
    new_user = User()
    new_user.id = req.uid
    new_user.username = req.username
    new_user.groups = req.group
    new_user.fullname = req.fullName
    new_user.avatar = req.avatar
    new_user.phone = req.phone
    new_user.email = req.email
    salt = token_utils.generate_random_string(32)
    refresh_token = token_utils.generate_random_string(512)
    enc_pass = token_utils.hash_password(req.password, salt)
    new_user.salt = salt
    new_user.password = enc_pass
    new_user.refresh_token = refresh_token

    await user_registry.user_add_direct(user=new_user)

    return {'message': 'success'}
