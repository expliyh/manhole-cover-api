from models import user_registry
from request_models import GetUserListOptions, UserResponse
from request_models.UserResponse import from_orm


async def list_user(options: GetUserListOptions):
    user_list = await user_registry.list_users(options)
    count = await user_registry.count(options)
    response = [from_orm(user) for user in user_list]
    return {
        'status': 'success',
        'user_list': response,
        'count': count
    }
