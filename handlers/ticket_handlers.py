from typing import Annotated

from fastapi import APIRouter, HTTPException, Header

import services
from models import user_registry, User
from request_models import UserResponse, LoginRequest, CreateTicketRequest
from token_utils import hash_password, generate_token

ticket_router = APIRouter()


@ticket_router.get("/api/ticket/get")
async def get_ticket(
        token: Annotated[str, Header()]
):
    pass


@ticket_router.post("/api/ticket/create")
async def create_ticket(
        request: CreateTicketRequest,
        token: Annotated[str, Header()]
):
    client_user = await user_registry.get_user_by_access_token(token)
    if client_user is None:
        raise HTTPException(status_code=401, detail="登录失效")
    if 'ADMIN' not in client_user.groups and 'EDITOR' not in client_user.groups:
        raise HTTPException(status_code=403, detail="权限不足")
    return await services.create_ticket(request)
