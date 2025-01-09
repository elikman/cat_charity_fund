from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_superuser, current_user
from app.crud import donation_crud, project_crud
from app.models import User
from app.schemas.donation import DonationCreate, DonationDB
from app.services.investing import investing

router = APIRouter()


@router.get('/',
            response_model=list[DonationDB],
            dependencies=[Depends(current_superuser)])
async def get_all_donations(
    session: AsyncSession = Depends(get_async_session)
):
    """Только для суперюзеров."""
    return await donation_crud.get_multi(session)


@router.post('/',
             response_model=DonationDB,
             response_model_exclude={
                 'invested_amount',
                 'fully_invested',
                 'close_date',
                 'user_id'},
             dependencies=[Depends(current_user)])
async def create_donation(
    donation: DonationCreate,
    session: AsyncSession = Depends(get_async_session)
):
    """Только для авторизированных пользователей."""
    new_donation = await donation_crud.create(donation, session)
    unfinished_projects = await project_crud.get_unfinished_objects(session)
    updated_donation, updated_projects = investing(
        new_donation, unfinished_projects
    )
    await donation_crud.save_updates(
        session, updated_donation, updated_projects
    )
    return updated_donation


@router.get('/my',
            response_model=list[DonationDB],
            response_model_exclude={
                'invested_amount',
                'fully_invested',
                'close_date',
                'user_id'},
            )
async def get_users_donation(
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user)
):
    """Для создателей объекта."""
    return await donation_crud.get_by_user(user=user, session=session)