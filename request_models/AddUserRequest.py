from pydantic import BaseModel


class AddUserRequest(BaseModel):
    uid: int
    username: str
    fullName: str
    email: str
    phone: str
    avatar: str
    disabled: bool
    group: list
    password: str
