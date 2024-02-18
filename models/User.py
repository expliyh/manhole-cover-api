from enum import Enum

from sqlalchemy import Column, Integer, String, JSON

from .ModelBase import model_base


class User(model_base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String)
    fullname = Column(String)
    password = Column(String)
    salt = Column(String)
    permissionOverride: dict = Column(JSON)

    def __repr__(self):
        return f"<User(name={self.name}, fullname={self.fullname}, password={self.password})>"
