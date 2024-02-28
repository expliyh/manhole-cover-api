from sqlalchemy import Column, String, Integer

from defines import Permission
from .ModelBase import model_base


class Group(model_base):
    __tablename__ = 'groups'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)
    generate_by = Column(String)
    p_config = Column(Integer)
    p_user = Column(Integer)
    p_group = Column(Integer)
    p_picture = Column(Integer)
    p_cover = Column(Integer)

    def __repr__(self):
        return f"<Group(name={self.name}, description={self.description})>"
