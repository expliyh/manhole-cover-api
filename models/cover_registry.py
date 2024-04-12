from fastapi import HTTPException
from sqlalchemy import select, func, update
from sqlalchemy.ext.asyncio import AsyncSession

from request_models.GetCoverListOptions import GetCoverListOptions
from defines import AuditStatus

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


async def get_list_by_uid(uid: int) -> list[Cover]:
    async with engine.new_session() as session:
        statement = select(Cover).where(Cover.uploadUser == uid)
        result = await session.execute(statement)
        return result.scalars().all()


async def list_covers(options: GetCoverListOptions) -> list[Cover]:
    """
    获取井盖列表
    :param options: 获取井盖列表的选项
    :return: 井盖列表
    """
    statement = select(Cover)
    try:
        for filter_option in options.filter_by:
            # if filter_option.field=="%ALL%":
            #     statement = statement.where(getattr(Cover))
            statement = statement.where(getattr(Cover, filter_option.field) == filter_option.value)
        for sort_option in options.sort_by:
            statement = statement.order_by(
                getattr(Cover, sort_option.field).asc() if sort_option.order == 'asc'
                else getattr(Cover, sort_option.field).desc()
            )
    except AttributeError as ex:
        raise ex
        # raise HTTPException(status_code=400, detail='Invalid filter or sort option')
    statement = statement.offset(options.first).limit(options.rows_per_page)
    cover_list: list[Cover] = []
    async with engine.new_session() as session:
        session: AsyncSession = session
        result = await session.execute(statement)
        for cover in result.scalars().all():
            cover_list.append(cover)
    return cover_list


async def reset_upload_user(old_uid: int, new_uid: int):
    statement = update(Cover).where(Cover.uploadUser == old_uid).values(uploadUser=new_uid)
    async with engine.new_session() as session:
        await session.execute(statement)
        await session.commit()


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
        await session.commit()
    return


async def set_ticket(cid: int, engineer: int):
    async with engine.new_session() as session:
        cover = await session.get(Cover, cid)
        if cover is None:
            raise HTTPException(status_code=404, detail='Cover not found')
        cover.ticketSentTo = engineer
        cover.auditStatus = AuditStatus.SENT_TICKET
        await session.commit()
    return
