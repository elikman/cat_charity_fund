#  app/api/endpoints/charity_project.py
from datetime import datetime
from typing import List

from fastapi import APIRouter, Body, Depends, Path
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import check_name_duplicate, check_invested_amount, \
    charity_project_exists, check_invested_summ, check_project_is_open
from app.core.db import get_async_session
from app.core.user import current_superuser
from app.crud import charity_project_crud, donation_crud
from app.schemas.charityproject import (CharityProjectCreate,
                                        CharityProjectRead,
                                        CharityProjectUpdate)
from app.services.investment import process_investment

router = APIRouter()


@router.get("/", response_model=List[CharityProjectRead])
async def get_charity_projects(
        session: AsyncSession = Depends(get_async_session)
):
    """
    Возвращает список всех проектов.
    """
    return await charity_project_crud.get_multi(session)


@router.post(
    "/",
    response_model=CharityProjectRead,
    dependencies=[Depends(current_superuser)]
)
async def create_project(
        project: CharityProjectCreate,
        session: AsyncSession = Depends(get_async_session),
):
    # Проверяем уникальность имени проекта
    await check_name_duplicate(project.name, session)
    # Создание проекта
    new_charity_project = await charity_project_crud.create(project, session)
    session.add_all(process_investment(
        new_charity_project, await donation_crud.get_opened(session))
    )
    await session.commit()
    await session.refresh(new_charity_project)
    return new_charity_project


@router.delete(
    "/{project_id}",
    response_model=CharityProjectRead,
    dependencies=[Depends(current_superuser)]
)
async def delete_project(
    project_id: int = Path(..., description="ID проекта для удаления"),
    session: AsyncSession = Depends(get_async_session)
):
    """
    Удаляет благотворительный проект. Доступно только для суперюзеров.
    Нельзя удалить проект, в который уже были инвестированы средства.
    """
    project = await charity_project_exists(project_id, session)
    await check_invested_amount(project_id, session)
    return await charity_project_crud.remove(project, session)


@router.patch(
    "/{project_id}",
    response_model=CharityProjectRead,
    dependencies=[Depends(current_superuser)],
    response_model_exclude_none=True,
)
async def update_project(
        project_id: int = Path(..., title="ID проекта"),
        project_update: CharityProjectUpdate = Body(...),
        session: AsyncSession = Depends(get_async_session),
):
    project = await charity_project_exists(project_id, session)
    if project_update.name:
        await check_name_duplicate(project_update.name, session)
    if project_update.full_amount:
        await check_invested_summ(
            project_id, project_update.full_amount, session
        )
    await check_project_is_open(project_id, session)
    project = await charity_project_crud.update(
        project, project_update, session
    )
    if project.full_amount == project.invested_amount:
        project.fully_invested = True
        project.close_date = datetime.now()
    else:
        session.add_all(
            process_investment(
                project,
                await donation_crud.get_opened(session))
        )
    await session.commit()
    await session.refresh(project)
    return project
