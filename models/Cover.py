from enum import Enum

from sqlalchemy import Column, Integer, String, JSON, DateTime

from .ModelBase import model_base


class Cover(model_base):
    __tablename__ = 'covers'
    id = Column(Integer, primary_key=True)
    picture_id = Column(Integer, foreign_key='pictures.id')
    latitude = Column(Integer)
    longitude = Column(Integer)
    positionFormat = Column(String, nullable=True)
    status = Column(String)
    auditStatus = Column(String)
    recognizeResult = Column(String)
    correctedResult = Column(String, nullable=True)
    uploadTime = Column(DateTime)
    recognizeTime = Column(DateTime)
    uploadUser = Column(Integer, foreign_key='users.id')
    editCount = Column(Integer)
    url = Column(String)

    def __repr__(self):
        return f"<Cover(latitude={self.latitude}, longitude={self.longitude}, url={self.url})>"
