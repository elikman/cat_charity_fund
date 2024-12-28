# app/models/charity_project.py

from sqlalchemy import Column, String, Text

from .finance_base import FinanceBase


class CharityProject(FinanceBase):
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text, nullable=False)

    def __repr__(self):
        return (
            f"{self.name}, {self.description}, {super().__repr__()}"
        )
