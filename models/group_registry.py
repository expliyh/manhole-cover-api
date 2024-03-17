from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from .engine import engine

from .Group import Group


async def get_group_by_id(gid: int) -> Group | None:
    async with engine.new_session() as session:
        session: AsyncSession = session
        result = await session.execute(select(Group).where(Group.id == gid))
        group = result.scalars().first()
        return group
