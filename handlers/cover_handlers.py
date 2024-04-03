from typing import Annotated

from fastapi import HTTPException, Header, APIRouter

from token_utils import get_uid_from_token
from models import user_registry
from models import group_registry
from request_models.GetCoverListOptions import GetCoverListOptions
from request_models.EditCoverRequest import EditCoverRequest
import services

router = APIRouter()


@router.post("/api/cover/list")
async def get_cover_list(
        options: GetCoverListOptions,
        token: Annotated[str | None, Header()] = None
):
    if token is None:
        raise HTTPException(status_code=401, detail="请登录")
    if options.rows_per_page > 1000:
        raise HTTPException(status_code=400, detail="Too many rows requested")
    user = await user_registry.get_user_by_access_token(token)
    if user is None:
        raise HTTPException(status_code=401, detail="登录失效，请重试")
    if "admin" not in user.groups:
        raise HTTPException(status_code=403, detail="权限不足")
    return await services.list_cover(options)


@router.post("/api/cover/edit")
async def edit_cover(
        option: EditCoverRequest,
        token: Annotated[str | None, Header()] = None
):
    if token is None:
        raise HTTPException(status_code=401, detail="请登录")
    user = await user_registry.get_user_by_access_token(token)
    if user is None:
        raise HTTPException(status_code=401, detail="登录失效，请重试")
    if "admin" not in user.groups:
        raise HTTPException(status_code=403, detail="权限不足")
    return await services.edit_cover(option)


@router.get("/api/cover/get")
async def get_cover(cid: int, token: Annotated[str | None, Header()] = None):
    return await services.get_cover(cid)
