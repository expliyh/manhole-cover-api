from request_models import DeleteUserRequest
from models import user_registry, cover_registry
from .generate_user_data import generate_user_data


async def delete_user(req: DeleteUserRequest):
    data_name = None
    if req.getData:
        data_name = await generate_user_data(req.uid)
    await cover_registry.reset_upload_user(req.uid, 2)
    await user_registry.delete_user(req.uid)
    return {
        "message": 'success',
        'data_name': data_name
    }
