from sqlalchemy import Column, String, Integer

from .ModelBase import model_base


class Group(model_base):
    __tablename__ = 'groups'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)
    generate_by = Column(String)

    def __repr__(self):
        return f"<Group(name={self.name}, description={self.description})>"