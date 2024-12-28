# api/crud/charity_project.py
from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.models import CharityProject
from app.schemas.charityproject import (CharityProjectCreate,
                                        CharityProjectUpdate)
from app.crud.base import CRUDBase


class CharityProjectCrud(
    CRUDBase[CharityProject, CharityProjectCreate, CharityProjectUpdate],
):
    async def get_project_by_name(
            self,
            session: AsyncSession,
            name: str
    ) -> Optional[CharityProject]:
        result = await session.execute(
            select(CharityProject).filter_by(name=name))
        return result.scalars().first()


charity_project_crud = CharityProjectCrud(CharityProject)
