import jwt

from fastapi import FastAPI, UploadFile, Request, HTTPException

from request_models.GetCoverListOptions import GetCoverListOptions

from models import user_registry

# create_database()

app = FastAPI()


# BEGIN DEFAULT API

@app.middleware('http')
async def auth(request: Request, call_next):
    token = request.headers.get('Token')
    uid = jwt.decode(token, options={"verify_signature": False})['uid']
    secret = user_registry.get_refresh_token(uid)
    if secret is None:
        raise HTTPException(status_code=400, detail="Invalid UID")
    try:
        jwt.decode(token, secret, algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=400, detail="Token expired")
    return call_next(request)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


# @app.post("/api/picture/add")
# async def new_picture(
#         picture: UploadFile,
#         longitude: float,
# ):
#     return {"message": "TODO: Return Picture ID"}


# @app.post("/api/cover-list/get")
# async def get_cover_list(
#         options: GetCoverListOptions
# ):
#     pass


@app.post("/api/position/get-formatted")
async def get_position_string(
        longitude: float,
        latitude: float
):
    return {"message": "TODO: Return Position String"}
