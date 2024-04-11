from pydantic import BaseModel


class UserEditRequest(BaseModel):
    uid: int | None = None
    username: str | None = None
    fullname: str | None = None
    phone: str | None = None
    email: str | None = None
