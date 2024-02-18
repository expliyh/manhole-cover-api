from enum import Enum

from sqlalchemy import Column, Integer, String, JSON

from .ModelBase import model_base


class Picture(model_base):
    __tablename__ = 'pictures'
    id = Column(Integer, primary_key=True)
    latitude = Column(Integer)
    longitude = Column(Integer)
    url = Column(String)
