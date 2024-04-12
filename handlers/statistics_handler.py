from typing import Annotated

from fastapi import APIRouter, HTTPException, Header
from models import user_registry, statistics
from request_models import UserResponse, LoginRequest
from token_utils import hash_password, generate_token

statistics_router = APIRouter()


@statistics_router.get("/api/statistics/all")
async def get_all_statistics(token: Annotated[str, Header()]):
    # Check if the user is authenticated
    user = await user_registry.get_user_by_access_token(token)
    if user is None:
        raise HTTPException(status_code=401, detail="登录失效")

    # Check if the user has admin privileges
    if 'ADMIN' not in user.groups:
        raise HTTPException(status_code=403, detail="权限不足")
    # Get the statistics
    return await statistics.get_statistics()
