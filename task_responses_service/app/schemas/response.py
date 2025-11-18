from pydantic import BaseModel, ConfigDict
from uuid import UUID
from datetime import datetime


class ResponseBase(BaseModel):
    task_title: str
    text: str


class ResponseCreate(ResponseBase):
    pass


class Response(ResponseBase):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    user_id: UUID
    status: str
    created_at: datetime
    updated_at: datetime

class ResponseList(BaseModel):
    items: list[Response]
    total: int