from sqlalchemy import create_engine

from sqlalchemy.ext.asyncio import create_async_engine

from .ModelBase import model_base


class Engine:
    def __init__(self):
        self.eg = create_async_engine("mariadb+asyncmy://dbcover:CG8k4s8XAzkWtPPC@db.irminsul.top:3306/dbcover")

        pass


def create_database():
    tmpeg = create_engine('mariadb+mariadbconnector://dbcover:CG8k4s8XAzkWtPPC@db.irminsul.top:3306/dbcover')

    model_base.metadata.create_all(tmpeg)


engine = create_async_engine("mariadb+asyncmy://dbcover:CG8k4s8XAzkWtPPC@db.irminsul.top:3306/dbcover")
