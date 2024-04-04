from enum import Enum

from sqlalchemy import Column, Integer, String, JSON, Boolean

import token_utils
from .Group import Group
from .ModelBase import model_base
from sqlalchemy.schema import Sequence


class User(model_base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=False)
    username = Column(String(32), index=True, unique=True)
    fullname = Column(String(64), nullable=True)
    email = Column(String(64), nullable=True, index=True, unique=True)
    phone = Column(String(11), nullable=True, index=True, unique=True)
    avatar = Column(String(2048), nullable=True)
    password = Column(String(512), nullable=True)
    refresh_token = Column(String(512), nullable=True, unique=True)
    groups: [str] = Column(JSON)
    disabled = Column(Boolean, default=False)
    salt = Column(String(32))

    def auth(self, password) -> bool:
        if self.password != token_utils.hash_password(password=password, salt=self.salt):
            return False
        else:
            return True

    def is_same(self, to_comp) -> bool:
        return (
                self.id == to_comp.id and
                self.username == to_comp.username and
                self.fullname == to_comp.fullname and
                self.email == to_comp.email and
                self.phone == to_comp.phone and
                self.avatar == to_comp.avatar and
                self.password == to_comp.password and
                self.refresh_token == to_comp.refresh_token and
                self.groups == to_comp.groups and
                self.disabled == to_comp.disabled and
                self.salt == to_comp.salt
        )

    def __repr__(self):
        return f"<User(name={self.name}, fullname={self.fullname}, password={self.password})>"


def _create_user(uid, username, password=None, fullname=None, email=None, phone=None,
                 avatar=None, refresh_token=None, groups=None, disabled=False, salt=None):
    user = User()
    user.id = uid
    user.username = username
    user.password = password
    user.fullname = fullname
    user.email = email
    user.phone = phone
    user.avatar = avatar
    user.refresh_token = refresh_token
    user.groups = groups or []  # 使用空列表作为默认值
    user.disabled = disabled
    user.salt = salt

    return user
