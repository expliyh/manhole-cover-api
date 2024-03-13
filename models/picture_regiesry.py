from sqlalchemy.ext.asyncio import AsyncSession

from sqlalchemy import select, update

from .Picture import Picture
from .engine import engine


async def add_picture(pic: Picture) -> int:
    async with engine.new_session() as session:
        session: AsyncSession = session
        session.add(pic)
        await session.commit()
        return pic.id


async def get_picture(pid: int) -> Picture | None:
    async with engine.new_session() as session:
        session: AsyncSession = session
        result = await session.execute(select(Picture).where(Picture.id == pid))
        pic = result.scalars().first()
        return pic


async def update_url(pid: int, url: str):
    async with engine.new_session() as session:
        session: AsyncSession = session
        await session.execute(update(Picture).where(Picture.id == pid).values(url=url))
    return
