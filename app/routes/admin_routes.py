from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.middleware.middleware import auth_middleware
from app.controllers.admin_controller import (
    create_admin,
    delete_admin,
    get_admin,
    get_all_admins,
    update_admin,
)
from app.db_config.db_connect import get_db
from app.models.admin import Admin
from app.schemas.admin_schema import AdminCreate

router = APIRouter()


@router.post("/admins/register", response_model=AdminCreate)
def create_admin_route(admin: AdminCreate, db: Session = Depends(get_db)):
    return create_admin(db=db, admin=admin)


@router.get(
    "/admins/{admin_id}",
    response_model=AdminCreate,
    dependencies=[Depends(auth_middleware)],
)
def read_admin_route(admin_id: int, db: Session = Depends(get_db)):
    return get_admin(db=db, admin_id=admin_id)


@router.get("/admins/", dependencies=[Depends(auth_middleware)])
def read_all_admins(db: Session = Depends(get_db)):
    return get_all_admins(db)


@router.put(
    "/admins/{admin_id}",
    response_model=AdminCreate,
    dependencies=[Depends(auth_middleware)],
)
def update_admin_route(
    admin_id: int, admin: AdminCreate, db: Session = Depends(get_db)
):
    admin_data = admin.model_dump(exclude_unset=True)
    return update_admin(db=db, admin_id=admin_id, admin_data=admin_data)


@router.delete("/admins/{admin_id}", dependencies=[Depends(auth_middleware)])
def delete_admin_route(admin_id: int, db: Session = Depends(get_db)):
    return delete_admin(db=db, admin_id=admin_id)
