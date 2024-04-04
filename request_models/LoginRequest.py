from pydantic import BaseModel


class LoginRequest(BaseModel):
    username: str | None
    password: str | None
