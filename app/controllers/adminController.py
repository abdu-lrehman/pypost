from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.admin import Admin
from ..schemas.adminSchema import AdminCreate
from passlib.context import CryptContext

# Configuration for Passlib
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str):
    return pwd_context.hash(password)


def create_admin(db: Session, admin: AdminCreate):
    hashed_password = hash_password(admin.password)

    admin_data = admin.model_dump(exclude={"password"})
    db_admin = Admin(**admin_data, password=hashed_password)

    db.add(db_admin)
    db.commit()
    db.refresh(db_admin)

    return db_admin


def update_admin(db: Session, admin_id: int, admin_data: dict):
    admin = db.query(Admin).filter(Admin.id == admin_id).first()
    if admin is None:
        raise HTTPException(status_code=404, detail="admin not found")

    if 'password' in admin_data:
        admin_data['password'] = hash_password(admin_data['password'])

    for field, value in admin_data.items():
        setattr(admin, field, value)

    db.commit()
    db.refresh(admin)
    return admin


def delete_admin(db: Session, admin_id: int):
    admin = db.query(Admin).filter(Admin.id == admin_id).first()
    if admin is None:
        raise HTTPException(status_code=404, detail="admin not found")

    db.delete(admin)
    db.commit()
    return {"message": "admin deleted successfully"}


def get_all_admins(db: Session):
    admin = db.query(Admin).all()
    return admin


def get_admin(db: Session, admin_id: int):

    admin = db.query(Admin).filter(Admin.id == admin_id).first()

    if admin is None:
        raise HTTPException(status_code=404, detail="admin not found")
    return admin
