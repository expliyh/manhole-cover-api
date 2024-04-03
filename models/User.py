from enum import Enum

from sqlalchemy import Column, Integer, String, JSON, Boolean

import token_utils
from .Group import Group
from .ModelBase import model_base


class User(model_base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(32))
    fullname = Column(String(64), nullable=True)
    email = Column(String(64), nullable=True)
    phone = Column(String(11), nullable=True)
    avatar = Column(String(2048), nullable=True)
    password = Column(String(512))
    refresh_token = Column(String(512))
    groups: [str] = Column(JSON)
    disabled = Column(Boolean, default=False)
    salt = Column(String(32))

    def auth(self, password) -> bool:
        if self.password != token_utils.hash_password(password=password, salt=self.salt):
            return False
        else:
            return True

    def __repr__(self):
        return f"<User(name={self.name}, fullname={self.fullname}, password={self.password})>"
