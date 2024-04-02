import re

from fastapi import HTTPException

from models import user_registry


async def reset_password(uid: int, new_password: str):
    if len(new_password) < 8:
        raise HTTPException(status_code=404, detail="密码太短")
    if not re.search(r"\d", new_password):
        raise HTTPException(status_code=400, detail="密码过于简单，至少包含一个大写字母、一个小写字母和一个数字")
    if not re.search(r"[A-Z]", new_password):
        raise HTTPException(status_code=400, detail="密码过于简单，至少包含一个大写字母、一个小写字母和一个数字")
    if not re.search(r"[a-z]", new_password):
        raise HTTPException(status_code=400, detail="密码过于简单，至少包含一个大写字母、一个小写字母和一个数字")
    # if not re.search(r"[!@#$%^&*(),.?\":{}|<>]",new_password):
    #     return False

    return await user_registry.reset_password(uid, new_password)
