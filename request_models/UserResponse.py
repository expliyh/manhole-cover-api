from pydantic import BaseModel


class UserResponse:
    username: str | None
    uid: int | None
    token: str | None
    role: None
    groups: [str]
