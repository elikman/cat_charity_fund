from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_superuser
from app.crud import donation_crud, project_crud
from app.schemas.charity_project import (CharityProjectCreate,
                                         CharityProjectDB,
                                         CharityProjectUpdate)
from app.services.investing import investing

from ..validators import check_name_duplicate, check_project_before_edit

router = APIRouter()


@router.get('/',
            response_model=list[CharityProjectDB])
async def get_all_charity_projects(
    session: AsyncSession = Depends(get_async_session)
):
    return await project_crud.get_multi(session)


@router.post('/',
             response_model=CharityProjectDB,
             dependencies=[Depends(current_superuser)])
async def create_charity_project(
    project: CharityProjectCreate,
    session: AsyncSession = Depends(get_async_session)
):
    """Только для суперюзеров."""
    await check_name_duplicate(project.name, session)
    new_project = await project_crud.create(
        project, session
    )
    unfinished_donations = await donation_crud.get_unfinished_objects(session)
    updated_project, updated_donations = investing(
        new_project, unfinished_donations
    )
    await donation_crud.save_updates(
        session, updated_project, updated_donations
    )
    return updated_project


@router.patch(
    '/{project_id}',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)]
)
async def update_charity_project(
    project_id: int,
    obj_in: CharityProjectUpdate,
    session: AsyncSession = Depends(get_async_session),
):
    """Только для суперюзеров."""
    project = await check_project_before_edit(project_id, session, obj_in)
    if obj_in.name is not None:
        await check_name_duplicate(obj_in.name, session)
    return await project_crud.update(
        project, obj_in, session
    )


@router.delete(
    '/{project_id}',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)]
)
async def delete_charity_project(
    project_id: int,
    session: AsyncSession = Depends(get_async_session)
):
    """Только для суперюзеров."""
    project = await check_project_before_edit(
        project_id=project_id, session=session
    )
    return await project_crud.remove(project, session)