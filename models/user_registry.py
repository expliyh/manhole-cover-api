from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

from sqlalchemy import select, update, func

import token_utils
from request_models import GetUserListOptions
from token_utils import hash_password
from .User import User, _create_user
from .engine import engine
from .default_users_strict import default_users_strict


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
    statement = select(User).where(User.id > 99)
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


async def delete_user(uid: int):
    async with engine.new_session() as session:
        to_delete = await session.get(User, uid)
        await session.delete(to_delete)
        await session.commit()


async def user_add_direct(user: User, no_check=False) -> User:
    if user.id < 100 and not no_check:
        raise HTTPException(status_code=400, detail="用户 ID 无效")
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
    # 注意：确保这里的 func.count() 用法是正确的，首先构建一个 select 语句
    statement = select(func.count()).select_from(User).filter(User.id > 99)

    try:
        for filter_option in options.filter_by:
            statement = statement.filter(getattr(User, filter_option.field) == filter_option.value)
    except AttributeError:
        raise HTTPException(status_code=400, detail='Invalid filter option')

    async with engine.new_session() as conn:  # 使用 begin() 以自动处理事务
        result = await conn.execute(statement)
        count_result = result.scalar()
        return count_result if count_result is not None else 0


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
                id=100,
                username='admin',
                password=enc_pass,
                refresh_token=refresh_token,
                email='admin@localhost',
                phone='12345678901',
                groups=['ADMIN'],
                salt=salt)
            session.add(default_admin)
            await session.commit()
            print('Default admin added')
        else:
            print('Default admin exists')

    for i in default_users_strict:
        d_user = await get_user_by_id(i.id)
        if d_user is None:
            try:
                await user_add_direct(i, True)
                continue
            except IntegrityError:
                raise RuntimeError("启动失败：系统关键保留用户被占用")
        else:
            if not d_user.is_same(i):
                raise RuntimeError("启动失败：系统关键保留用户被占用")


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
