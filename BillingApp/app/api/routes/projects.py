import uuid

from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_current_user_id
from app.schemas.project import ProjectCreate, ProjectResponse, ProjectUpdate
from app.services.project_service import (
    create_new_project,
    get_all_projects,
    get_project,
    remove_project,
    update_project_details,
)

router = APIRouter(prefix="/projects", tags=["Projects"])


@router.get("/", response_model=list[ProjectResponse])
def projects(db: Session = Depends(get_db), user_id: uuid.UUID = Depends(get_current_user_id)):
    return get_all_projects(db, user_id)


@router.get("/{project_id}", response_model=ProjectResponse)
def project_by_id(project_id: uuid.UUID, db: Session = Depends(get_db), user_id: uuid.UUID = Depends(get_current_user_id)):
    return get_project(db, project_id, user_id)


@router.post("/", response_model=ProjectResponse, status_code=status.HTTP_201_CREATED)
def create(data: ProjectCreate, db: Session = Depends(get_db), user_id: uuid.UUID = Depends(get_current_user_id)):
    return create_new_project(db, user_id, **data.model_dump())


@router.put("/{project_id}", response_model=ProjectResponse)
def update(project_id: uuid.UUID, data: ProjectUpdate, db: Session = Depends(get_db), user_id: uuid.UUID = Depends(get_current_user_id)):
    return update_project_details(db, project_id, user_id, **data.model_dump(exclude_unset=True))


@router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete(project_id: uuid.UUID, db: Session = Depends(get_db), user_id: uuid.UUID = Depends(get_current_user_id)):
    remove_project(db, project_id, user_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
