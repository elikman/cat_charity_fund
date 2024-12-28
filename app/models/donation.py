# app/models/donation.py
from sqlalchemy import Column, ForeignKey, Integer, String

from .finance_base import FinanceBase


class Donation(FinanceBase):
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    comment = Column(String, nullable=True)

    def __repr__(self):
        return (
            f"{self.user_id}, {self.comment}, {super().__repr__()}"
        )
