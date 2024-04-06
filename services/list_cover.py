from models import cover_registry, user_registry
from request_models.GetCoverListOptions import GetCoverListOptions


async def list_cover(options: GetCoverListOptions):
    cover_list = await cover_registry.list_covers(options)
    name_dict = {}
    for i in cover_list:
        name_dict[i.uploadUser] = (await user_registry.get_user_by_id(i.uploadUser)).fullname
    count = await cover_registry.count(options)

    return {
        'status': 'success',
        'cover_list': cover_list,
        'username_dict': name_dict,
        'count': count
    }
