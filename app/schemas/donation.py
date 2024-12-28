from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Extra, PositiveInt


class DonationBase(BaseModel):
    full_amount: PositiveInt
    comment: Optional[str]

    class Config:
        extra = Extra.forbid


class DonationCreate(DonationBase):
    pass


class DonationDB(DonationBase):
    id: int
    create_date: Optional[datetime]
    invested_amount: Optional[int] = 0
    fully_invested: Optional[bool] = False
    close_date: Optional[datetime]
    user_id: Optional[int]

    class Config:
        orm_mode = True