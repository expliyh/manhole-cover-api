from typing import List

from pydantic import BaseModel

from datetime import datetime


class CoverInfo:
    id: int
    positionFormat: str
    auditStatus: str
    image: str
    status: str
    recognizeResult: str
    correctedResult: str | None
    uploadTime: datetime | None
    recognizeTime: datetime | None
    uploadUser: str
    editCount: int | None
