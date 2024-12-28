# app/schemas/charity_project.py
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Extra, Field, PositiveInt, constr


class CharityProjectBase(BaseModel):
    name: str
    description: str
    full_amount: int


class CharityProjectCreate(CharityProjectBase):
    name: str = Field(
        ..., max_length=100, min_length=1, example="Сбор на еду для пушистых"
    )
    description: str = Field(..., min_length=1)
    full_amount: PositiveInt = Field(..., example=5000)


class CharityProjectUpdate(CharityProjectBase):
    name: Optional[constr(min_length=1, max_length=100)] = None
    description: Optional[constr(min_length=1)] = None
    full_amount: Optional[PositiveInt] = None

    class Config:
        extra = Extra.forbid


class CharityProjectRead(CharityProjectBase):
    id: int
    invested_amount: int
    fully_invested: bool
    create_date: datetime
    close_date: Optional[datetime]

    class Config:
        orm_mode = True
