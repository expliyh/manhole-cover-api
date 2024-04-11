from typing import Annotated

from fastapi import APIRouter, HTTPException, Header
from models import user_registry, User
from request_models import UserResponse, LoginRequest
from token_utils import hash_password, generate_token

login_router = APIRouter()


@login_router.post('/api/login')
async def login(
        req: LoginRequest
):
    user: User = await user_registry.get_user_by_username(req.username)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    if not user.auth(req.password):
        raise HTTPException(status_code=403, detail="Password incorrect")
    user_response = UserResponse(
        username=user.username,
        uid=user.id,
        token=generate_token(user.id, user.refresh_token),
        role=None,
        full_name=user.fullname,
        groups=user.groups
    )
    return user_response


@login_router.get('/api/ping')
async def access_token_auth(
        token: Annotated[str | None, Header()] = None
):
    if token is None:
        raise HTTPException(status_code=401, detail="请登录")
    user = await user_registry.get_user_by_access_token(token)
    if user is None:
        raise HTTPException(status_code=401, detail="登录失效，请重试")
    user_response = UserResponse(
        username=user.username,
        uid=user.id,
        token=generate_token(user.id, user.refresh_token),
        role=None,
        full_name=user.fullname,
        groups=user.groups
    )
    return user_response
