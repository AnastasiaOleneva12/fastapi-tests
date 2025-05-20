from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class TaskCreate(BaseModel):
    title: str = Field(..., example='Сделать дз')
    description: Optional[str] = Field(None, example='Разобрать теорию, начать выполнение задания...')
    status: str = Field('в ожидании', example='в работе')
    priority: Optional[int] = Field(None, example=1)


class TaskResponse(TaskCreate):
    id: int
    created_at: datetime
    model_config = {'from_attributes': True}