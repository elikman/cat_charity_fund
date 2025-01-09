from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_superuser, current_user
from app.crud.donation import donation_crud
from app.models import User
from app.schemas.donation import DonationBase, DonationCreate, DonationDB
#from app.services.investing import investing_process

router = APIRouter()

@router.post('/',
             response_model=DonationCreate,
             response_model_exclude_none=True
             )
async def create_donation(donation: DonationBase,
                          session: AsyncSession = Depends(get_async_session),
                          user: User = Depends(current_user)
                          ):
    """Сделать пожертвование."""
    return await donation_crud.create(donation, session, user)


@router.get(
    '/my',
    response_model=list[DonationCreate],
    response_model_exclude={'user_id'},
)
async def get_user_donations(
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user)
):
    """Вернуть список пожертвований пользователя, выполняющего запрос."""
    return await donation_crud.get_by_user(
        session=session, user=user
    )


@router.get(
    '/',
    response_model=list[DonationDB],
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
)
async def get_all_donations(
    session: AsyncSession = Depends(get_async_session),
):
    """Только для суперюзеров.

    Возвращает список всех пожертвований.
    """
    return await donation_crud.get_multi(session)
