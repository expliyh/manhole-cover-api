from enum import Enum

from sqlalchemy import Column, Integer, String, JSON, DateTime, Text, ForeignKey

from .ModelBase import model_base


class Cover(model_base):
    __tablename__ = 'covers'
    id = Column(Integer, primary_key=True)
    picture_id = Column(Integer, ForeignKey('pictures.id'))
    latitude = Column(Integer)
    longitude = Column(Integer)
    positionFormat = Column(Text, nullable=True)
    status = Column(String(32))
    auditStatus = Column(String(32))
    recognizeResult = Column(String(16))
    correctedResult = Column(String(16), nullable=True)
    uploadTime = Column(DateTime)
    recognizeTime = Column(DateTime)
    uploadUser = Column(Integer, ForeignKey('users.id'))
    editCount = Column(Integer)
    url = Column(Text)

    def __repr__(self):
        return f"<Cover(latitude={self.latitude}, longitude={self.longitude}, url={self.url})>"
