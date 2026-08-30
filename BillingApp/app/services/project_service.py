import uuid

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.project import Project
from app.repositories.project_repository import (
    create_project,
    delete_project,
    get_project_by_code,
    get_project_by_id_and_user,
    get_projects,
    update_project,
)


def create_new_project(db: Session, user_id: uuid.UUID, **data) -> Project:
    if get_project_by_code(db, user_id, data["project_code"]):
        raise HTTPException(status_code=409, detail="Project code already exists")
    project = Project(id=uuid.uuid4(), user_id=user_id, **data)
    return create_project(db, project)


def get_all_projects(db: Session, user_id: uuid.UUID) -> list[Project]:
    return get_projects(db, user_id)


def get_project(db: Session, project_id: uuid.UUID, user_id: uuid.UUID) -> Project:
    project = get_project_by_id_and_user(db, project_id, user_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project


def update_project_details(db: Session, project_id: uuid.UUID, user_id: uuid.UUID, **data) -> Project:
    project = get_project(db, project_id, user_id)
    if "project_code" in data and data["project_code"] != project.project_code:
        existing = get_project_by_code(db, user_id, data["project_code"])
        if existing and existing.id != project.id:
            raise HTTPException(status_code=409, detail="Project code already exists")
    for field, value in data.items():
        if value is not None:
            setattr(project, field, value)
    return update_project(db, project)


def remove_project(db: Session, project_id: uuid.UUID, user_id: uuid.UUID) -> None:
    project = get_project(db, project_id, user_id)
    try:
        delete_project(db, project)
    except Exception as exc:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Project cannot be deleted because it is used by existing bills",
        ) from exc
