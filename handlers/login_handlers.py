from fastapi import APIRouter, HTTPException
from models import user_registry, User
from request_models import UserResponse
from token_utils import hash_password, generate_token

login_router = APIRouter()


@login_router.post('/api/login')
async def login(
        username: str,
        password: str
):
    user: User = await user_registry.get_user_by_username(username)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    password_secure = hash_password(password)
    if user.password != password_secure:
        raise HTTPException(status_code=403, detail="Password incorrect")
    user_response = UserResponse(
        username=user.username,
        uid=user.id,
        token=generate_token(user.id, user.refresh_token),
        role=None,
        groups=user.groups
    )
    return user_response
