from typing import Annotated

from fastapi import APIRouter, Header, HTTPException

import token_utils
from models import user_registry
import services
from request_models import GetUserListOptions, UidRequest, EditPasswordRequest

router = APIRouter()


@router.post("/api/user/list")
async def get_user_list(
        options: GetUserListOptions,
        token: Annotated[str | None, Header()] = None
):
    # if token is None:
    #     raise HTTPException(status_code=401, detail="Authorization required")
    # if options.rows_per_page > 1000:
    #     raise HTTPException(status_code=400, detail="Too many rows requested")
    # uid = get_uid_from_token(token)
    # user = await get_user_by_id(uid)
    # group = await group_registry.get_group_by_id(user.group_id)
    # if not group.p_list_cover:
    #     raise HTTPException(status_code=403, detail="Permission denied")
    return await services.list_user(options)


@router.get("/api/user/get")
async def get_user(
        uid: int,
        token: Annotated[str | None, Header()] = None
):
    # if token is None:
    #     raise HTTPException(status_code=401, detail="Authorization required")
    # uid = get_uid_from_token(token)
    # if uid != uid:
    #     raise HTTPException(status_code=403, detail="Permission denied")
    return await services.get_user(uid)


@router.post("/api/user/edit/disable")
async def disable_user(
        req: UidRequest,
        token: Annotated[str | None, Header()] = None
):
    # if token is None:
    #     raise HTTPException(status_code=401, detail="Authorization required")
    # uid = get_uid_from_token(token)
    # if uid != uid:
    #     raise HTTPException(status_code=403, detail="Permission denied")
    await user_registry.disable_user(req.uid)
    return {"status": "success"}


@router.post("/api/user/edit/enable")
async def enable_user(
        req: UidRequest,
        token: Annotated[str | None, Header()] = None
):
    # if token is None:
    #     raise HTTPException(status_code=401, detail="Authorization required")
    # uid = get_uid_from_token(token)
    # if uid != uid:
    #     raise HTTPException(status_code=403, detail="Permission denied")
    # print(req)
    await user_registry.enable_user(req.uid)
    return {"status": "success"}


@router.post("/api/user/edit/password")
async def edit_password(
        req: EditPasswordRequest,
        token: Annotated[str | None, Header()] = None
):
    if req.old_password is None:
        client_uid = token_utils.get_uid_from_token(token)
        client_user = await user_registry.get_user_by_id(client_uid)
        if 'admin' not in client_user.groups:
            raise HTTPException(status_code=401, detail="请输入旧密码")
    else:
        async with user_registry.get_user_by_id(req.uid) as user:
            if not user.auth(req.old_password):
                raise HTTPException(status_code=401, detail="旧密码错误")

    return await services.reset_password(req.uid, req.new_password)
