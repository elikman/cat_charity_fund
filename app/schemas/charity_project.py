from datetime import datetime
from typing import Optional

from pydantic import (
    BaseModel,
    Field,
    PositiveInt,
    Extra,
)
from pydantic.types import StrictInt

from app.schemas.constans import (
    MIN_NAME_LENGTH,
    MAX_NAME_LENGTH,
    DEFAULT_FULL_AMOUNT_1,
    DEFAULT_FULL_AMOUNT_2,
)

class CharityProjectBase(BaseModel):
    name: Optional[str] = Field(
        None, min_length=MIN_NAME_LENGTH, max_length=MAX_NAME_LENGTH
    )
    description: Optional[str] = Field(None, min_length=MIN_NAME_LENGTH)
    full_amount: Optional[PositiveInt]

    class Config:
        extra = Extra.forbid


class CharityProjectCreate(CharityProjectBase):
    name: str = Field(min_length=MIN_NAME_LENGTH, max_length=MAX_NAME_LENGTH)
    description: str = Field(min_length=MIN_NAME_LENGTH)
    full_amount: PositiveInt
    invested_amount: int = 0

    class Config:
        extra = Extra.forbid
        schema_extra = {
            "example": {
                "name": "Сбор средств для кошечек",
                "description": "На всё хорошее",
                "full_amount": DEFAULT_FULL_AMOUNT_1,
            }
        }


class CharityProjectUpdate(CharityProjectBase):
    class Config:
        schema_extra = {
            "example": {
                "name": "Новое имя проекта",
                "description": "Новое описание проекта",
                "full_amount": DEFAULT_FULL_AMOUNT_2,
            }
        }


class CharityProjectDB(CharityProjectCreate):
    id: int
    invested_amount: StrictInt
    fully_invested: bool = False
    create_date: datetime
    close_date: Optional[datetime]

    class Config:
        orm_mode = True
