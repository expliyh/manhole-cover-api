from sqlalchemy import Column, Integer, String, JSON, Text, DECIMAL, DateTime, ForeignKey, Enum

from defines import PictureStatus

from .ModelBase import model_base


class Picture(model_base):
    __tablename__ = 'pictures'
    id = Column(Integer, primary_key=True, autoincrement=True)
    status = Column(Enum(PictureStatus), default=PictureStatus.UPLOADED, nullable=False)
    latitude = Column(DECIMAL(9, 6))
    longitude = Column(DECIMAL(9, 6))
    position_format = Column(Text)
    uploadTime = Column(DateTime)
    recognizeTime = Column(DateTime, nullable=True)
    upload_user = Column(Integer, ForeignKey('users.id'), nullable=True)
    url = Column(Text, nullable=True)
