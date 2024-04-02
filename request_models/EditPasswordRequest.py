from pydantic import BaseModel


class EditPasswordRequest(BaseModel):
    uid: int
    new_password: str
    old_password: str | None
