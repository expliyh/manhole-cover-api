from typing import Annotated

from fastapi import APIRouter, HTTPException, Header

from config import get_uid_from_token
from models.user_registry import get_user_by_id
from request_models.GetCoverListOptions import GetCoverListOptions
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
    # TODO: 检查用户权限
    return await services.list_cover(options)
    pass
