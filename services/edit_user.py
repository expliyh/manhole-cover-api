from fastapi import HTTPException

from models import user_registry
from request_models import UserEditRequest
from request_models.UserResponse import from_orm


async def edit_user(req: UserEditRequest, target_uid: int | None):
    if target_uid is not None and req.uid is not None and target_uid != req.uid:
        raise HTTPException(status_code=400, detail="参数冲突")
    if req.uid is not None:
        target_uid = req.uid
    user = await user_registry.get_user_by_id(target_uid)
    if user is None:
        raise HTTPException(status_code=404, detail="用户不存在")
    user.username = req.username or user.username
    user.fullname = req.fullname or user.fullname
    user.email = req.email or user.email
    user.phone = req.phone or user.phone
    # user.avatar = req.avatar or user.avatar
    await user_registry.merge(user)

    return from_orm(user)
