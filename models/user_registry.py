from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from sqlalchemy import select, update, func

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


async def get_user_by_access_token(token: str) -> User | None:
    uid = token_utils.get_uid_from_token(token)
    user = await get_user_by_id(uid)
    if user is None:
        return None
    if not token_utils.verify_token(token, user.refresh_token):
        return None
    return user


async def get_user_by_email(email: str) -> User | None:
    async with engine.new_session() as session:
        result = await session.execute(select(User).where(User.email == email))
        user = result.scalars().first()
        return user


async def get_user_by_username(username: str) -> User | None:
    async with engine.new_session() as session:
        result = await session.execute(select(User).where(User.username == username))
        user = result.scalar()
        return user


async def get_user_by_phone(phone: str) -> User | None:
    async with engine.new_session() as session:
        result = await session.execute(select(User).where(User.phone == phone))
        user = result.scalars().first()
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
    refresh_token = token_utils.generate_random_string(512)
    enc_pass = hash_password(password, salt)
    async with engine.new_session() as session:
        user = User(username=username, password=enc_pass, refresh_token=refresh_token, groups=groups, salt=salt)
        session.add(user)
        await session.commit()
        return user


async def user_add_direct(user: User) -> User:
    async with engine.new_session() as session:
        session.add(user)
        await session.commit()
        return user


async def count(options: GetUserListOptions) -> int:
    """
    获取井盖列表的数量
    :param options: 获取井盖列表的选项
    :return: 井盖列表的数量
    """
    statement = func.count(User.id)
    try:
        for filter_option in options.filter_by:
            statement = statement.where(getattr(User, filter_option.field) == filter_option.value)
    except AttributeError:
        raise HTTPException(status_code=400, detail='Invalid filter option')
    async with engine.new_session() as session:
        result = await session.execute(statement)
        return result.scalar()


async def disable_user(uid: int) -> None:
    async with engine.new_session() as session:
        await session.execute(update(User).where(User.id == uid).values(disabled=True))
        await session.commit()


async def enable_user(uid: int) -> None:
    async with engine.new_session() as session:
        await session.execute(update(User).where(User.id == uid).values(disabled=False))
        await session.commit()


async def check_default_user() -> None:
    salt = token_utils.generate_random_string(32)
    refresh_token = token_utils.generate_random_string(512)
    enc_pass = hash_password('admin', salt)
    async with engine.new_session() as session:
        result = await session.execute(select(User).where(User.username == 'admin'))
        user = result.scalars().first()
        if user is None:
            default_admin = User(
                username='admin',
                password=enc_pass,
                refresh_token=refresh_token,
                email='admin@localhost',
                phone='12345678901',
                groups=['ADMIN'],
                salt=salt)
            session.add(default_admin)
            await session.commit()
            print('Default user added')
        else:
            print('Default user exists')


async def reset_password(uid: int, new_password: str):
    salt = token_utils.generate_random_string(32)
    refresh_token = token_utils.generate_random_string(512)
    enc_pass = hash_password(new_password, salt)
    if uid <= 0:
        raise HTTPException(status_code=400, detail="此用户不可被编辑")
    async with engine.new_session() as session:
        user: User | None = await session.get(uid)
        if user is None:
            raise HTTPException(status_code=404, detail="找不到用户")
        user.refresh_token = refresh_token
        user.salt = salt
        user.password = enc_pass
        await session.commit()
