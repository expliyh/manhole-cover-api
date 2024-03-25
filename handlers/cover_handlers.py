from typing import Annotated

from fastapi import HTTPException, Header, APIRouter

from config import get_uid_from_token
from models.user_registry import get_user_by_id
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
        raise HTTPException(status_code=401, detail="Authorization required")
    if options.rows_per_page > 1000:
        raise HTTPException(status_code=400, detail="Too many rows requested")
    uid = get_uid_from_token(token)
    user = await get_user_by_id(uid)
    group = await group_registry.get_group_by_id(user.group_id)
    if not group.p_list_cover:
        raise HTTPException(status_code=403, detail="Permission denied")
    return await services.list_cover(options)


@router.post("/api/cover/edit")
async def edit_cover(option: EditCoverRequest):
    return await services.edit_cover(option)


@router.get("/api/cover/get")
async def get_cover(cid: int, token: Annotated[str | None, Header()] = None):
    return await services.get_cover(cid)
