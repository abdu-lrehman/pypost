from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from ..dbconfig.dbconnect import get_db
from ..models.admin import Admin
from ..schemas.adminSchema import AdminCreate
from ..controllers.adminController import create_admin, get_admin, update_admin, delete_admin, get_all_admins

router = APIRouter()


@router.post("/admins/register", response_model=AdminCreate)
def create_admin_route(admin: AdminCreate, db: Session = Depends(get_db)):
    return create_admin(db=db, admin=admin)


@router.get("/admins/{admin_id}", response_model=AdminCreate)
def read_admin_route(admin_id: int, db: Session = Depends(get_db)):
    return get_admin(db=db, admin_id=admin_id)


@router.get("/admins/")
def read_all_admins(db: Session = Depends(get_db)):
    return get_all_admins(db)


@router.put("/admins/{admin_id}", response_model=AdminCreate)
def update_admin_route(admin_id: int, admin: AdminCreate, db: Session = Depends(get_db)):
    admin_data = admin.model_dump(exclude_unset=True)
    return update_admin(db=db, admin_id=admin_id, admin_data=admin_data)


@router.delete("/admins/{admin_id}")
def delete_admin_route(admin_id: int, db: Session = Depends(get_db)):
    return delete_admin(db=db, admin_id=admin_id)
