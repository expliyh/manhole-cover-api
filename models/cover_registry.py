from fastapi import HTTPException
from sqlalchemy import select, func, update
from sqlalchemy.ext.asyncio import AsyncSession

from request_models.GetCoverListOptions import *

from .engine import engine
from .Cover import Cover


async def add_cover(cover: Cover) -> int:
    """
    向数据库中添加一个井盖
    :param cover: 要添加的井盖
    :return: 自动分配或提前设置的id
    """
    return await engine.add(cover)


async def get_cover(cid: int) -> Cover | None:
    """
    通过id获取井盖
    :param cid: 井盖的id
    :return: 井盖
    """
    async with engine.new_session() as session:
        session: AsyncSession = session
        result = await session.execute(select(Cover).where(Cover.id == cid))
        cover = result.scalars().first()
        return cover


async def list_covers(options: GetCoverListOptions) -> list[Cover]:
    """
    获取井盖列表
    :param options: 获取井盖列表的选项
    :return: 井盖列表
    """
    statement = select(Cover)
    try:
        for filter_option in options.filter_by:
            statement = statement.where(getattr(Cover, filter_option.field) == filter_option.value)
        for sort_option in options.sort_by:
            statement = statement.order_by(
                getattr(Cover, sort_option.field).asc() if sort_option.order == 'asc'
                else getattr(Cover, sort_option.field).desc()
            )
    except AttributeError:
        raise HTTPException(status_code=400, detail='Invalid filter or sort option')
    statement = statement.offset(options.first).limit(options.rows_per_page)
    cover_list: list[Cover] = []
    async with engine.new_session() as session:
        session: AsyncSession = session
        result = await session.execute(statement)
        for cover in result.scalars().all():
            cover_list.append(cover)
    return cover_list


async def list_covers_by_pid(pid: int) -> list[Cover]:
    statement = select(Cover).where(Cover.picture_id == pid)
    async with engine.new_session() as session:
        session: AsyncSession = session
        result = await session.execute(statement)
        cover_list: list[Cover] = []
        for cover in result.scalars().all():
            cover_list.append(cover)
        return cover_list


async def count(options: GetCoverListOptions) -> int:
    """
    获取井盖列表的数量
    :param options: 获取井盖列表的选项
    :return: 井盖列表的数量
    """
    statement = func.count(Cover.id)
    try:
        for filter_option in options.filter_by:
            statement = statement.where(getattr(Cover, filter_option.field) == filter_option.value)
    except AttributeError:
        raise HTTPException(status_code=400, detail='Invalid filter option')
    async with engine.new_session() as session:
        session: AsyncSession = session
        result = await session.execute(statement)
        return result.scalar()


async def update_url(cid: int, url: str):
    async with engine.new_session() as session:
        session: AsyncSession = session
        await session.execute(update(Cover).where(Cover.id == cid).values(url=url))
    return
