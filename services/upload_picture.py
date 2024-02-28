from fastapi import UploadFile


async def upload_picture(
        latitude: int,
        longitude: int,
        position_format: str,
        picture: UploadFile
):