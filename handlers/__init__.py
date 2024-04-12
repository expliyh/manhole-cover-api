from .cover_handlers import router as cover_router
from .file_handlers import file_router
from .picture_handlers import router as picture_router
from .geo_handlers import router as geo_router
from .login_handlers import login_router
from .user_handlers import router as user_router
from .ticket_handlers import ticket_router

routers = [cover_router, picture_router, geo_router, login_router, file_router, user_router, ticket_router]
