from datetime import datetime
from typing import Optional

from pydantic import (
    BaseModel,
    Field,
    PositiveInt,
    Extra,
)
from pydantic.types import StrictInt

from app.core.constans import (
    MIN_LENGTH_NAME,
    MAX_LENGTH_NAME,
    MIN_NAME_LENGTH,
    MAX_NAME_LENGTH,
    FULL_AMOUNT_DEFAULT,
    FULL_AMOUNT_UPDATE
)


class CharityProjectBase(BaseModel):
    name: Optional[str] = Field(
        None, min_length=MIN_LENGTH_NAME, max_length=MAX_LENGTH_NAME
    )
    description: Optional[str] = Field(None, min_length=MIN_LENGTH_NAME)
    full_amount: Optional[PositiveInt]

    class Config:
        extra = Extra.forbid


class CharityProjectCreate(CharityProjectBase):
    name: str = Field(min_length=MIN_NAME_LENGTH, max_length=MAX_NAME_LENGTH)
    description: str = Field(min_length=MIN_NAME_LENGTH)
    full_amount: PositiveInt
    invested_amount: int = 0

    class Config:
        schema_extra = {
            "example": {
                "name": "Сбор средств для кошечек",
                "description": "На всё хорошее",
                "full_amount": FULL_AMOUNT_DEFAULT,
            }
        }


class CharityProjectUpdate(CharityProjectBase):
    class Config:
        schema_extra = {
            "example": {
                "name": "Новое имя проекта",
                "description": "Новое описание проекта",
                "full_amount": FULL_AMOUNT_UPDATE,
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
