from sqlalchemy import Column, String, Text

from app.core.constants import MAX_LENGTH_NAME

from .base import CharityProjectDonationBase


class CharityProject(CharityProjectDonationBase):
    name = Column(String(MAX_LENGTH_NAME), unique=True, nullable=False)
    description = Column(Text, nullable=False)
