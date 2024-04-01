from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from sqlalchemy import select, update

import token_utils
from request_models import GetUserListOptions
from token_utils import hash_password
from .User import User
from .engine import engine


async def get_refresh_token(uid: int) -> str | None:
    async with engine.new_session() as session:
        result = await session.execute(select(User).where(User.id == uid))
        user = result.scalars().first()
        return user.refresh_token if user is not None else None


async def get_user_by_id(uid: int) -> User | None:
    async with engine.new_session() as session:
        result = await session.execute(select(User).where(User.id == uid))
        user = result.scalars().first()
        return user


async def get_user_by_username(username: str) -> User | None:
    async with engine.new_session() as session:
        result = await session.execute(select(User).where(User.username == username))
        user = result.scalar()
        return user


async def list_users(options: GetUserListOptions) -> list[User]:
    """
    获取井盖列表
    :param options: 获取井盖列表的选项
    :return: 井盖列表
    """
    statement = select(User)
    try:
        for filter_option in options.filter_by:
            # if filter_option.field=="%ALL%":
            #     statement = statement.where(getattr(Cover))
            statement = statement.where(getattr(User, filter_option.field) == filter_option.value)
        for sort_option in options.sort_by:
            statement = statement.order_by(
                getattr(User, sort_option.field).asc() if sort_option.order == 'asc'
                else getattr(User, sort_option.field).desc()
            )
    except AttributeError as _:
        # raise ex
        raise HTTPException(status_code=400, detail='Invalid filter or sort option')
    statement = statement.offset(options.first).limit(options.rows_per_page)
    user_list: list[User] = []
    async with engine.new_session() as session:
        result = await session.execute(statement)
        for user in result.scalars().all():
            user_list.append(user)
    return user_list


async def add_user(username: str, password: str, groups: [str]) -> User:
    salt = token_utils.generate_random_string(32)
    enc_pass = hash_password(password, salt)
    async with engine.new_session() as session:
        user = User(username=username, password=enc_pass, groups=groups, salt=salt)
        session.add(user)
        await session.commit()
        return user


async def check_default_user() -> None:
    async with engine.new_session() as session:
        result = await session.execute(select(User).where(User.username == 'admin'))
        user = result.scalars().first()
        if user is None:
            await add_user('admin', 'admin', ['admin'])
            print('Default user added')
        else:
            print('Default user exists')
