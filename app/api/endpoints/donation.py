# app/api/endpoints/donation.py
from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_superuser, current_user
from app.crud import donation_crud, charity_project_crud
from app.schemas.donation import DonationCreate, DonationRead, DonationReadPost
from app.services.investment import process_investment

router = APIRouter()


@router.get(
    "/",
    response_model=List[DonationRead],
    dependencies=[Depends(current_superuser)]
)
async def get_donations(session: AsyncSession = Depends(get_async_session)):
    """
    Возвращает список всех пожертвований.
    Доступно только для суперпользователей.
    """
    return await donation_crud.get_multi(session)


@router.post(
    "/",
    response_model=DonationReadPost,
    summary="Create Donation")
async def create_donation(
        donation_data: DonationCreate,
        session: AsyncSession = Depends(get_async_session),
        user=Depends(current_user)
):
    """
    Создать новое пожертвование.
    """
    new_donation = await donation_crud.create(donation_data, session, user)
    session.add_all(process_investment(
        new_donation, await charity_project_crud.get_opened(session)
    ))
    await session.commit()
    await session.refresh(new_donation)
    return new_donation


@router.get(
    "/my",
    response_model=List[DonationReadPost],
    summary="Get User Donations",
    description=(
            "Вернуть список пожертвований пользователя, выполняющего запрос."
    )
)
async def get_user_donations(
    session: AsyncSession = Depends(get_async_session),
    user=Depends(current_user)
):
    """
    Возвращает список всех пожертвований текущего пользователя.
    """
    return await donation_crud.get_donations_by_user(session, user.id)
