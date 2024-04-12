from pydantic import BaseModel


class CreateTicketRequest(BaseModel):
    tid: str | None = None
    engineer: int
    cover: int
