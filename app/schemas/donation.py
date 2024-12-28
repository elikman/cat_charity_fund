# app/schemas/donation.py
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Extra, PositiveInt


class DonationBase(BaseModel):
    user_id: int
    full_amount: int
    comment: Optional[str] = None


class DonationCreate(BaseModel):
    full_amount: PositiveInt
    comment: Optional[str] = None


class DonationUpdate(DonationBase):
    full_amount: Optional[int] = None
    comment: Optional[str] = None


class DonationReadPost(BaseModel):
    id: int
    full_amount: int
    comment: Optional[str] = None
    create_date: datetime

    class Config:
        orm_mode = True
        extra = Extra.forbid


class DonationRead(BaseModel):
    id: int
    full_amount: int
    comment: Optional[str] = None
    create_date: datetime
    invested_amount: Optional[int] = 0
    fully_invested: Optional[bool] = False
    user_id: Optional[int] = None
    close_date: Optional[datetime] = None

    class Config:
        orm_mode = True
        extra = Extra.forbid
