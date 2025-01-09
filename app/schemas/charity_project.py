from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Extra, Field, PositiveInt, validator
from pydantic.fields import Required

from app.core.constants import MAX_LENGTH_NAME


class CharityProjectBase(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=MAX_LENGTH_NAME)
    description: Optional[str]
    full_amount: Optional[PositiveInt]

    class Config:
        extra = Extra.forbid


class CharityProjectCreate(CharityProjectBase):
    name: str = Field(Required, min_length=1, max_length=MAX_LENGTH_NAME)
    description: str = Field(Required, min_length=1)
    full_amount: PositiveInt

    class Config:
        extra = Extra.forbid
        schema_extra = {
            "example": {
                "name": "string",
                "description": "string",
                "full_amount": 0
            }
        }


class CharityProjectUpdate(CharityProjectBase):
    @validator('name', 'description', 'full_amount')
    def name_cannot_be_null(cls, value, field):
        if not value:
            raise ValueError(f'{field} не может быть пустым!')
        return value


class CharityProjectDB(CharityProjectBase):
    id: int
    invested_amount: Optional[int] = 0
    fully_invested: Optional[bool] = False
    create_date: Optional[datetime]
    close_date: Optional[datetime]

    class Config:
        orm_mode = True