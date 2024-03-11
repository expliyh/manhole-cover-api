from sqlalchemy import Column, String, Integer, ForeignKey

from defines import Permission
from .ModelBase import model_base


class Group(model_base):
    __tablename__ = 'groups'
    id = Column(Integer, primary_key=True)
    name = Column(String(64))
    description = Column(String(128))
    generate_by = Column(Integer,ForeignKey("users.id"))
    p_config = Column(Integer)
    p_user = Column(Integer)
    p_group = Column(Integer)
    p_picture = Column(Integer)
    p_cover = Column(Integer)

    def __repr__(self):
        return f"<Group(name={self.name}, description={self.description})>"
