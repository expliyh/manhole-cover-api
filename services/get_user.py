from models import user_registry
from request_models.UserResponse import from_orm, UserResponse


async def get_user(uid: int, include_token: bool = False) -> UserResponse | None:
    user = await user_registry.get_user_by_id(uid)
    if user is None:
        return None
    return from_orm(user, include_token)
