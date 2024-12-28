from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import project_crud
from app.models import CharityProject
from app.schemas.charity_project import CharityProjectUpdate


async def check_project_before_edit(
        project_id: int,
        session: AsyncSession,
        obj_in: CharityProjectUpdate = None,

) -> CharityProject:
    project = await project_crud.get(project_id, session)
    if not project:
        raise HTTPException(
            status_code=404,
            detail='Проект не найден!'
        )

    if project.fully_invested:
        raise HTTPException(
            status_code=400,
            detail='Проект полностью проинвестирован!',
        )
    if obj_in and obj_in.full_amount:
        if obj_in.full_amount < project.invested_amount:
            raise HTTPException(
                status_code=422,
                detail=f'В проект уже внесено {project.invested_amount}',
            )
    elif not obj_in:
        if project.invested_amount > 0:
            raise HTTPException(
                status_code=400,
                detail='Проект имеет инвестиции!',
            )
    return project


async def check_invested_amount(
        project_id: int,
        session: AsyncSession
) -> None:
    project = await project_crud.get(project_id, session)
    if project.invested_amount > 0:
        raise HTTPException(
            status_code=400,
            detail='Проект имеет инвестиции!',
        )


async def check_name_duplicate(
        project_name: str,
        session: AsyncSession
) -> None:
    project_id = await project_crud.get_object_by_name(project_name, session)
    if project_id is not None:
        raise HTTPException(
            status_code=400,
            detail='Проект с таким именем уже существует!',
        )