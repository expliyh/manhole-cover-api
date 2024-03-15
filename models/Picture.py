from enum import Enum

from sqlalchemy import Column, Integer, String, JSON, Text, DECIMAL

from .ModelBase import model_base


class Picture(model_base):
    __tablename__ = 'pictures'
    id = Column(Integer, primary_key=True, autoincrement=True)
    latitude = Column(DECIMAL(9, 6))
    longitude = Column(DECIMAL(9, 6))
    position_format = Column(Text)
    url = Column(Text, nullable=True)
