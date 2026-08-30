import uuid

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.project import Project


def get_project_by_id(db: Session, project_id: uuid.UUID) -> Project | None:
    return db.scalar(select(Project).where(Project.id == project_id))


def get_project_by_id_and_user(
    db: Session,
    project_id: uuid.UUID,
    user_id: uuid.UUID,
) -> Project | None:
    return db.scalar(
        select(Project).where(
            Project.id == project_id,
            Project.user_id == user_id,
        )
    )


def get_projects(db: Session, user_id: uuid.UUID) -> list[Project]:
    return list(
        db.scalars(
            select(Project)
            .where(Project.user_id == user_id)
            .order_by(Project.project_name)
        ).all()
    )


def get_project_by_code(
    db: Session,
    user_id: uuid.UUID,
    project_code: str,
) -> Project | None:
    return db.scalar(
        select(Project).where(
            Project.user_id == user_id,
            Project.project_code == project_code,
        )
    )


def create_project(db: Session, project: Project) -> Project:
    db.add(project)
    db.commit()
    db.refresh(project)
    return project


def update_project(db: Session, project: Project) -> Project:
    db.commit()
    db.refresh(project)
    return project


def delete_project(db: Session, project: Project) -> None:
    db.delete(project)
    db.commit()
