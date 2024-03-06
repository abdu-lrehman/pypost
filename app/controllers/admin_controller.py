from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from app.db_config.db_connect import get_db
from app.middleware.admin_dependency import admin_dependency
from app.models.admin import Admin
from app.models.book import Book
from app.models.records import Records
from app.models.user import User
from app.schemas.admin_schema import AdminCreate
from app.schemas.book_schema import BookCreate
from app.schemas.user_schema import UserCreate

router = APIRouter()


def __hash_password(password: str):
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    return pwd_context.hash(password)


@router.get("/", dependencies=[Depends(admin_dependency)])
def get_all_admins(db: Session = Depends(get_db)):
    admin = db.query(Admin).all()
    return admin


@router.get(
    "/{admin_id}",
    response_model=AdminCreate,
    dependencies=[Depends(admin_dependency)],
)
def get_admin(admin_id: int, db: Session = Depends(get_db)):

    admin = db.query(Admin).filter(Admin.id == admin_id).first()

    if admin is None:
        raise HTTPException(status_code=404, detail="admin not found")
    return admin


@router.post("/", response_model=AdminCreate)
def create_admin(admin: AdminCreate, db: Session = Depends(get_db)):
    hashed_password = __hash_password(admin.password)

    admin_data = admin.model_dump(exclude={"password"})
    db_admin = Admin(**admin_data, password=hashed_password)

    db.add(db_admin)
    db.commit()
    db.refresh(db_admin)

    return db_admin


@router.put(
    "/{admin_id}",
    response_model=AdminCreate,
    dependencies=[Depends(admin_dependency)],
)
def update_admin(admin_id: int, admin: AdminCreate, db: Session = Depends(get_db)):
    admin_data = admin.model_dump(exclude_unset=True)
    admin = db.query(Admin).filter(Admin.id == admin_id).first()
    if admin is None:
        raise HTTPException(status_code=404, detail="admin not found")

    if "password" in admin_data:
        admin_data["password"] = __hash_password(admin_data["password"])

    for field, value in admin_data.items():
        setattr(admin, field, value)

    db.commit()
    db.refresh(admin)
    return admin


@router.delete("/{admin_id}", dependencies=[Depends(admin_dependency)])
def delete_admin(admin_id: int, db: Session = Depends(get_db)):
    admin = db.query(Admin).filter(Admin.id == admin_id).first()
    if admin is None:
        raise HTTPException(status_code=404, detail="admin not found")

    db.delete(admin)
    db.commit()
    return {"message": "admin deleted successfully"}


@router.get("/user/", dependencies=[Depends(admin_dependency)])
def get_all_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return users


@router.get(
    "/user/{user_id}",
    response_model=UserCreate,
    dependencies=[Depends(admin_dependency)],
)
def get_user(user_id: int, db: Session = Depends(get_db)):

    user = db.query(User).filter(User.id == user_id).first()

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.get("/record/user", dependencies=[Depends(admin_dependency)])
def get_all_records(db: Session = Depends(get_db)):
    records = db.query(Records).all()
    return records


@router.get(
    "/record/user/{user_id}",
    dependencies=[Depends(admin_dependency)],
)
def get_user_records(user_id: int, db: Session = Depends(get_db)):

    records = db.query(Records).filter(Records.user_id == user_id).first()

    if records is None:
        raise HTTPException(status_code=404, detail="user has no records")
    return records


@router.get(
    "/record/book/{book_id}",
    dependencies=[Depends(admin_dependency)],
)
def get_book_records(book_id: int, db: Session = Depends(get_db)):

    records = db.query(Records).filter(Records.book_id == book_id).first()

    if records is None:
        raise HTTPException(status_code=404, detail="Book has no records")
    return records
