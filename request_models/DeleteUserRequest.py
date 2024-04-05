from pydantic import BaseModel


class DeleteUserRequest(BaseModel):
    uid: int
    getData: bool
