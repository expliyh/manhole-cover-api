from enum import Enum

from sqlalchemy import Column, Integer, String, JSON

from .ModelBase import model_base


class User(model_base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(32))
    fullname = Column(String(64))
    password = Column(String(32))
    salt = Column(String(256))
    permissionOverride: dict = Column(JSON)

    def __repr__(self):
        return f"<User(name={self.name}, fullname={self.fullname}, password={self.password})>"
