from sqlalchemy.ext.asyncio import AsyncSession

from sqlalchemy import select, update

from .User import User
from .engine import engine


async def get_refresh_token(uid: int) -> str | None:
    async with engine.new_session() as session:
        session: AsyncSession = session
        result = await session.execute(select(User).where(User.id == uid))
        user = result.scalars().first()
        return user.refresh_token if user is not None else None


async def get_user_by_id(uid: int) -> User | None:
    async with engine.new_session() as session:
        session: AsyncSession = session
        result = await session.execute(select(User).where(User.id == uid))
        user = result.scalars().first()
        return user


async def get_user_by_username(username: str) -> User | None:
    async with engine.new_session() as session:
        session: AsyncSession = session
        result = await session.execute(select(User).where(User.username == username))
        user = result.scalar()
        return user
