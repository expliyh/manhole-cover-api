from pydantic import BaseModel


class UidRequest(BaseModel):
    uid: int
