# app/crud/donation.py
from typing import List

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.models import Donation
from app.schemas.donation import DonationCreate, DonationReadPost

from app.crud.base import CRUDBase


class DonationCrud(
    CRUDBase[Donation, DonationCreate, DonationReadPost],
):
    async def get_donations_by_user(
            self,
            session: AsyncSession,
            user_id: int
    ) -> List[Donation]:
        result = await session.execute(
            select(Donation).where(Donation.user_id == user_id)
        )
        return result.scalars().all()


donation_crud = DonationCrud(Donation)
