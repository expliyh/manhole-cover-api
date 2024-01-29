from fastapi import FastAPI, UploadFile

app = FastAPI()


# BEGIN DEFAULT API

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


# BEGIN RESTFUL API


@app.post("/api/picture")
async def new_picture(
        picture: UploadFile,
        longitude: float,
        latitude: float
):
    return {"message": "TODO: Return Picture ID"}


# BEGIN OTHER API

@app.post("/api/position/get-formatted")
async def get_position_string(
        longitude: float,
        latitude: float
):
    return {"message": "TODO: Return Position String"}
