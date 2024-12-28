# app/models/finance_base.py
from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, Integer, CheckConstraint

from app.core.db import Base


class FinanceBase(Base):
    full_amount = Column(Integer, nullable=False)
    invested_amount = Column(Integer, default=0)
    fully_invested = Column(Boolean, default=False)
    create_date = Column(DateTime, default=datetime.now)
    close_date = Column(DateTime, nullable=True)

    __abstract__ = True

    __table_args__ = (
        CheckConstraint('full_amount > 0',
                        name='check_full_amount_positive'),
        CheckConstraint('invested_amount <= full_amount',
                        name='check_invested_amount_not_exceed'),
        CheckConstraint('invested_amount >= 0',
                        name='check_invested_amount_positive'),
    )

    def __repr__(self):
        return (
            f"{self.full_amount}, {self.invested_amount},"
            f"{self.fully_invested}, {self.create_date},"
            f"{self.close_date}"
        )
