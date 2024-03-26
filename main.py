import logging
from contextlib import asynccontextmanager

import jwt

from fastapi import FastAPI, UploadFile, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from request_models.GetCoverListOptions import GetCoverListOptions

from recognize import yolo

from models import user_registry, engine

from handlers import routers

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)


# BEGIN DEFAULT API

# @app.middleware('http')
# async def auth(request: Request, call_next):
#     token = request.headers.get('Token')
#     uid = jwt.decode(token, options={"verify_signature": False})['uid']
#     secret = user_registry.get_refresh_token(uid)
#     if secret is None:
#         raise HTTPException(status_code=400, detail="Invalid UID")
#     try:
#         jwt.decode(token, secret, algorithms=["HS256"])
#     except jwt.ExpiredSignatureError:
#         raise HTTPException(status_code=400, detail="Token expired")
#     return call_next(request)

@asynccontextmanager
async def lifespan(app: FastAPI):
    await engine.create_all()
    yolo.init_model('recognize/best.onnx')
    yield


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


@app.post("/api/position/get-formatted")
async def get_position_string(
        longitude: float,
        latitude: float
):
    return {"message": "TODO: Return Position String"}


for i in routers:
    app.include_router(i)
