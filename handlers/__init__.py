from .cover_handlers import router as cover_router
from .picture_handlers import router as picture_router
from .geo_handlers import router as geo_router

routers = [cover_router, picture_router, geo_router]
