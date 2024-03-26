from fastapi import APIRouter
from models import user_registry

login_router = APIRouter()


@login_router.post('/api/login')
async def login(
        username: str,
        password: str
):
    # TODO: 验证请求并返回用户信息
    pass
