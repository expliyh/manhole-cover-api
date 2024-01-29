from fastapi import FastAPI, UploadFile

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


@app.post("/api/picture")
async def new_picture(
        picture: UploadFile,
        longitude: float,
        latitude: float,
        token: str
):
    return {"message": "TODO: Return Picture ID"}
