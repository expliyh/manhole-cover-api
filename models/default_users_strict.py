from .User import User, _create_user

default_users_strict: list[User] = [
    _create_user(
        2,
        username='deleted',
        fullname='已删除的用户',
        disabled=True
    )
]
