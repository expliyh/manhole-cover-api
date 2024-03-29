import hashlib

import jwt


def get_uid_from_token(token: str):
    return jwt.decode(token, options={"verify_signature": False})['uid']


def generate_token(uid: int, refresh_token: str):
    return jwt.encode({'uid': uid}, refresh_token, algorithm='HS256')


def hash_password(password: str):
    return hashlib.sha512(password.encode('utf-8')).hexdigest()
