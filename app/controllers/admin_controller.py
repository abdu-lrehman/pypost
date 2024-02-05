from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, HTTPException
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

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str):
    return pwd_context.hash(password)


@router.get("/admin/get_all_admins/", dependencies=[Depends(admin_dependency)])
def get_all_admins(db: Session = Depends(get_db)):
    admin = db.query(Admin).all()
    return admin


@router.get(
    "/admin/find_admin/{admin_id}",
    response_model=AdminCreate,
    dependencies=[Depends(admin_dependency)],
)
def get_admin(admin_id: int, db: Session = Depends(get_db)):

    admin = db.query(Admin).filter(Admin.id == admin_id).first()

    if admin is None:
        raise HTTPException(status_code=404, detail="admin not found")
    return admin


@router.post("/admin/register_admin", response_model=AdminCreate)
def create_admin(admin: AdminCreate, db: Session = Depends(get_db)):
    hashed_password = hash_password(admin.password)

    admin_data = admin.model_dump(exclude={"password"})
    db_admin = Admin(**admin_data, password=hashed_password)

    db.add(db_admin)
    db.commit()
    db.refresh(db_admin)

    return create_admin(db=db, admin=admin)


@router.put(
    "/admin/update_admin/{admin_id}",
    response_model=AdminCreate,
    dependencies=[Depends(admin_dependency)],
)
def update_admin(admin_id: int, admin: AdminCreate, db: Session = Depends(get_db)):
    admin_data = admin.model_dump(exclude_unset=True)
    admin = db.query(Admin).filter(Admin.id == admin_id).first()
    if admin is None:
        raise HTTPException(status_code=404, detail="admin not found")

    if "password" in admin_data:
        admin_data["password"] = hash_password(admin_data["password"])

    for field, value in admin_data.items():
        setattr(admin, field, value)

    db.commit()
    db.refresh(admin)
    return admin


@router.delete(
    "/admin/delete_admin/{admin_id}", dependencies=[Depends(admin_dependency)]
)
def delete_admin(admin_id: int, db: Session = Depends(get_db)):
    admin = db.query(Admin).filter(Admin.id == admin_id).first()
    if admin is None:
        raise HTTPException(status_code=404, detail="admin not found")

    db.delete(admin)
    db.commit()
    return {"message": "admin deleted successfully"}


@router.post(
    "/admin/create_book/",
    response_model=BookCreate,
    dependencies=[Depends(admin_dependency)],
)
def create_book(book_data: BookCreate, db: Session = Depends(get_db)):
    db_book = Book(
        title=book_data.title,
        author=book_data.author,
        published_date=book_data.published_date,
        borrowed_by_id=None,
    )

    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book


@router.get(
    "/admin/find_book/{book_id}",
    response_model=BookCreate,
    dependencies=[Depends(admin_dependency)],
)
def get_book(book_id: int, db: Session = Depends(get_db)):
    db_book = db.query(Book).filter(Book.id == book_id).first()
    if db_book.borrowed_at + timedelta(hours=24) < datetime.utcnow():
        db_book.borrowed_at = None
        db_book.borrowed_by_id = None
        db.commit()
        db.refresh(db_book)
    return db_book


@router.get("/admin/get_all_books/", dependencies=[Depends(admin_dependency)])
def get_all_books(db: Session = Depends(get_db)):
    books = db.query(Book).all()
    return books


@router.put(
    "/admin/update_book/{book_id}",
    response_model=BookCreate,
    dependencies=[Depends(admin_dependency)],
)
def update_book(book_id: int, updated_data: BookCreate, db: Session = Depends(get_db)):
    db_book = db.query(Book).filter(Book.id == book_id).first()
    if db_book:
        db_book.title = updated_data.title
        db_book.author = updated_data.author
        db_book.published_date = updated_data.published_date
        db_book.borrowed_by_id = updated_data.borrowed_by_id
        db.commit()
        db.refresh(db_book)
    return db_book


@router.delete("/admin/delete_book/{book_id}", dependencies=[Depends(admin_dependency)])
def delete_book(book_id: int, db: Session = Depends(get_db)):
    db_book = db.query(Book).filter(Book.id == book_id).first()
    if db_book:
        db.delete(db_book)
        db.commit()
    return db_book


@router.get("/admin/get_all_users/", dependencies=[Depends(admin_dependency)])
def get_all_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return users


@router.get(
    "/admin/get_user/{user_id}",
    response_model=UserCreate,
    dependencies=[Depends(admin_dependency)],
)
def get_user(user_id: int, db: Session = Depends(get_db)):

    user = db.query(User).filter(User.id == user_id).first()

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.get("/admin/get_all_records/", dependencies=[Depends(admin_dependency)])
def get_all_records(db: Session = Depends(get_db)):
    records = db.query(Records).all()
    return records


@router.get(
    "/admin/get_user_records/{user_id}",
    dependencies=[Depends(admin_dependency)],
)
def get_user_records(user_id: int, db: Session = Depends(get_db)):

    records = db.query(Records).filter(Records.user_id == user_id).first()

    if records is None:
        raise HTTPException(status_code=404, detail="user has no records")
    return records


@router.get(
    "/admin/get_book_records/{book_id}",
    dependencies=[Depends(admin_dependency)],
)
def get_book_records(book_id: int, db: Session = Depends(get_db)):

    records = db.query(Records).filter(Records.book_id == book_id).first()

    if records is None:
        raise HTTPException(status_code=404, detail="Book has no records")
    return records
