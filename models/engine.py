from sqlalchemy import create_engine, MetaData, select, func, text

from sqlalchemy.ext.asyncio import (
    create_async_engine,
    AsyncSession,
    AsyncConnection,
    async_sessionmaker
)

from .ModelBase import model_base


class Engine:
    def __init__(self):
        self.eg = create_async_engine(
            "mariadb+asyncmy://dbcover:CG8k4s8XAzkWtPPC@db.irminsul.top:3306/dbcover",

        )

    async def create_all(self):
        async with self.eg.begin() as conn:
            await conn.run_sync(model_base.metadata.create_all)
        # await self.set_autoincrement_start('users')

    def new_session(self) -> AsyncSession:
        return async_sessionmaker(self.eg, expire_on_commit=True)()

    async def add(self, obj) -> int:
        async with async_sessionmaker(self.eg, expire_on_commit=False)() as session:
            session.add(obj)
            await session.commit()
            oid = obj.id
            session.expire_all()
            return oid


engine = Engine()
