from fastapi import UploadFile
from pydantic import BaseModel


class UploadPictureRequest(BaseModel):
    latitude: str
    longitude: str
    position_format: str
