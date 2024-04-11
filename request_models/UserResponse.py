from pydantic import BaseModel
from models import User
import token_utils


class UserResponse:
    username: str | None
    uid: int | None
    avatar: str | None
    email: str | None
    full_name: str | None
    phone: str | None
    token: str | None
    role: None | str
    disabled: bool
    groups: [str]

    def __init__(self, username: str | None = None, uid: int | None = None, avatar: str | None = None,
                 email: str | None = None, phone: str | None = None, token: str | None = None, role: None | str = None,
                 disabled: bool = False, groups: [str] = None, full_name: str | None = None):
        self.username = username
        self.uid = uid
        self.avatar = avatar
        self.email = email
        self.phone = phone
        self.token = token
        self.role = role
        self.disabled = disabled
        self.groups = groups
        self.full_name = full_name


def from_orm(user: User, include_token=False) -> UserResponse:
    return UserResponse(
        username=user.username,
        uid=user.id,
        token=token_utils.generate_token(user.id, user.refresh_token) if include_token else None,
        email=user.email,
        phone=user.phone,
        disabled=user.disabled,
        avatar=user.avatar if user.avatar else "https://vip.123pan.cn/1814176066/DirectLink/%E8%8A%99%E5%8D%A1%E6%B4%9B%E6%96%AF_QuAn.jpg",
        role="Depreciated",
        groups=user.groups,
        full_name=user.fullname
    )
