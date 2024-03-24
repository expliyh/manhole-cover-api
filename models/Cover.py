from sqlalchemy import Column, Integer, String, JSON, DateTime, Text, ForeignKey, Enum

from .ModelBase import model_base

from defines import AuditStatus


class Cover(model_base):
    __tablename__ = 'covers'
    id = Column(Integer, primary_key=True)
    picture_id = Column(Integer, ForeignKey('pictures.id'))
    latitude = Column(Integer)
    longitude = Column(Integer)
    positionFormat = Column(Text, nullable=True)
    status = Column(String(32))
    auditStatus = Column(Enum(AuditStatus), default=AuditStatus.NOT_VIEWED, nullable=False)
    recognizeResult = Column(String(16))
    correctedResult = Column(String(16), nullable=True)
    uploadTime = Column(DateTime)
    recognizeTime = Column(DateTime)
    uploadUser = Column(Integer, ForeignKey('users.id'))
    editCount = Column(Integer)
    url = Column(Text, nullable=True)

    def __repr__(self):
        return f"<Cover(latitude={self.latitude}, longitude={self.longitude}, url={self.url})>"
