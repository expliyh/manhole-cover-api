from models import cover_registry
from request_models.GetCoverListOptions import GetCoverListOptions


async def list_cover(options: GetCoverListOptions):
    cover_list = cover_registry.list_covers(options)
    count = cover_registry.count(options)

    return {
        'status': 'success',
        'cover_list': cover_list,
        'count': count
    }