from typing import List

from pydantic import BaseModel


class EditCoverRequest(BaseModel):
    """
    编辑井盖时所需的参数
    """
    cid: int
    auditStatus: str | None
    correctedResult: str | None
