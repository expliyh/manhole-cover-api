from enum import Enum

from sqlalchemy import Column, Integer, String, JSON

from .Group import Group
from .ModelBase import model_base


class User(model_base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(32))
    fullname = Column(String(64), nullable=True)
    password = Column(String(512))
    refresh_token = Column(String(512), nullable=True)
    groups: [str] = Column(JSON)
    salt = Column(String(32))

    def __repr__(self):
        return f"<User(name={self.name}, fullname={self.fullname}, password={self.password})>"
