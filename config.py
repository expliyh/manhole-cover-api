import jwt

file_path = './covers/'

allow_picture_exts = ('png', 'jpg', 'jpeg', 'gif', 'webp', 'bmp')


def get_uid_from_token(token: str):
    return jwt.decode(token, options={"verify_signature": False})['uid']
