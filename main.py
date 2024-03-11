from fastapi import FastAPI, UploadFile

from request_models.GetCoverListOptions import GetCoverListOptions

from models import create_database

create_database()

app = FastAPI()


# BEGIN DEFAULT API

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


@app.post("/api/picture/add")
async def new_picture(
        picture: UploadFile,
        longitude: float,
):
    return {"message": "TODO: Return Picture ID"}


@app.post("/api/cover-list/get")
async def get_cover_list(
        options: GetCoverListOptions
):
    pass


@app.post("/api/position/get-formatted")
async def get_position_string(
        longitude: float,
        latitude: float
):
    return {"message": "TODO: Return Position String"}
