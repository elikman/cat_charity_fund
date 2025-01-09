from sqlalchemy import Column, ForeignKey, Integer, Text

from .base import CharityProjectDonationBase


class Donation(CharityProjectDonationBase):
    comment = Column(Text)
    user_id = Column(Integer, ForeignKey('user.id'))