import hashlib
import random
import string
import time

import jwt
from jwt import InvalidTokenError


def get_uid_from_token(token: str):
    return jwt.decode(token, options={"verify_signature": False})['uid']


def verify_token(token: str, refresh_token: str) -> bool:
    try:
        jwt.decode(token, refresh_token, algorithms='HS256')
    except InvalidTokenError:
        return False
    return True


def generate_token(uid: int, refresh_token: str) -> str:
    return str(jwt.encode({'uid': uid}, refresh_token, algorithm='HS256'))


def hash_password(password: str, salt: str):
    return hashlib.sha256((password + salt).encode('utf-8')).hexdigest()


def generate_random_string(length):
    random.seed(time.time())  # 使用当前时间戳作为随机种子
    letters = string.ascii_letters + string.digits
    random_string = ''.join(random.choice(letters) for _ in range(length))
    return random_string
