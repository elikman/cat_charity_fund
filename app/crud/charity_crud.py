from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from app.models import CharityProject
from app.schemas.charity_project import CharityProjectCreate, CharityProjectUpdate

class CharityCrud:
    async def create(self, obj_in: CharityProjectCreate, session: AsyncSession) -> CharityProject:
        new_obj = CharityProject(**obj_in.dict())
        session.add(new_obj)
        try:
            await session.commit()  # Выполняем commit
            await session.refresh(new_obj)  # Выполняем refresh
        except IntegrityError as e:
            await session.rollback()
            raise e
        return new_obj

    async def patch(self, db_obj: CharityProject, obj_in: CharityProjectUpdate, session: AsyncSession) -> CharityProject:
        for field, value in obj_in.dict(exclude_unset=True).items():
            setattr(db_obj, field, value)
        try:
            await session.commit()
            await session.refresh(db_obj)
        except IntegrityError as e:
            await session.rollback()
            raise e
        return db_obj

    async def delete(self, db_obj: CharityProject, session: AsyncSession) -> CharityProject:
        await session.delete(db_obj)
        try:
            await session.commit()
        except IntegrityError as e:
            await session.rollback()
            raise e
        return db_obj
