from pydantic import BaseModel


class UserResponse:
    username: str | None
    uid: int | None
    token: str | None
    role: None
    groups: [str]

    def __init__(self, username: str, uid: int, token: str, role: None, groups: [str]):
        self.username = username
        self.uid = uid
        self.token = token
        self.role = role
        self.groups = groups
