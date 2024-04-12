from fastapi import HTTPException

from models import user_registry, cover_registry
from request_models import CreateTicketRequest


async def create_ticket(
        req: CreateTicketRequest
):
    user = await user_registry.get_user_by_id(req.engineer)
    if user is None:
        raise HTTPException(status_code=404, detail="维修员不存在")
    await cover_registry.set_ticket(req.cover, req.engineer)
    return {
        'message': 'success'
    }
