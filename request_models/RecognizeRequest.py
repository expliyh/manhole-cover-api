from typing import List

from pydantic import BaseModel


class RecognizeRequest(BaseModel):
    pid: int
