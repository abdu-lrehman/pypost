from datetime import datetime, timedelta

from fastapi import APIRouter, Body, Depends, HTTPException
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from app.db_config.db_connect import get_db
from app.middleware.user_dependency import user_dependency
from app.models.book import Book
from app.models.records import Records
from app.models.user import User
from app.schemas.book_schema import BookCreate
from app.schemas.user_schema import UserCreate

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

router = APIRouter()


def hash_password(password: str):
    return pwd_context.hash(password)


@router.post("/user/register_user", response_model=UserCreate)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    hashed_password = hash_password(user.password)

    user_data = user.model_dump(exclude={"password"})
    db_user = User(**user_data, password=hashed_password)

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user


@router.put(
    "/user/update_user/{user_id}",
    response_model=UserCreate,
    dependencies=[Depends(user_dependency)],
)
def update_user(user_id: int, user: UserCreate, db: Session = Depends(get_db)):
    user_data = user.model_dump(exclude_unset=True)
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    if "password" in user_data:
        user_data["password"] = hash_password(user_data["password"])

    for field, value in user_data.items():
        setattr(user, field, value)

    db.commit()
    db.refresh(user)
    return user


@router.delete("/user/delete_user/{user_id}", dependencies=[Depends(user_dependency)])
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    db.delete(user)
    db.commit()
    return {"message": "User deleted successfully"}


@router.get(
    "/user/get_book/{book_id}",
    response_model=BookCreate,
    dependencies=[Depends(user_dependency)],
)
def get_book(
    book_id: int,
    db: Session = Depends(get_db),
    decoded_token: dict = Depends(user_dependency),
):
    db_book = db.query(Book).filter(Book.id == book_id).first()

    if db_book.borrowed_at + timedelta(hours=24) < datetime.utcnow():
        db_book.borrowed_at = None
        db_book.borrowed_by_id = None
        db.commit()
        db.refresh(db_book)

    if decoded_token.id == db_book.borrowed_by_id:
        return db_book

    response_data = {
        "id": db_book.id,
        "title": db_book.title,
        "author": db_book.author,
        "published_date": db_book.published_date,
        "borrowed_at": db_book.borrowed_at,
        "borrowed_by_id": db_book.borrowed_by_id,
    }
    return response_data


@router.get("/user/get_all_books/", dependencies=[Depends(user_dependency)])
def get_all_books(db: Session = Depends(get_db)):
    books = db.query(Book).defer(Book.content).all()
    return books


@router.put(
    "/user/borrow_book/{book_id}",
    dependencies=[Depends(user_dependency)],
)
def borrow_book(book_id: int, user_id: int, db: Session = Depends(get_db)):
    db_book = db.query(Book).filter(Book.id == book_id).first()

    if db_book.borrowed_by_id is None:
        db_book.borrowed_by_id = user_id
        db.commit()
        db.refresh(db_book)
        record = Records(book_id=book_id, user_id=user_id)
        db.add(record)
        db.commit()
        db.refresh(record)
    return "book borrowed"


@router.put(
    "/user/return_book/{book_id}",
    dependencies=[Depends(user_dependency)],
)
def return_book(book_id: int, user_id: int, db: Session = Depends(get_db)):
    db_book = db.query(Book).filter(Book.id == book_id).first()
    if db_book.borrowed_by_id == user_id:
        db_book.borrowed_by_id == None
        db.commit()
        db.refresh(db_book)

    return "book borrowed"


@router.get(
    "/user/get_user_records/{user_id}",
    dependencies=[Depends(user_dependency)],
)
def get_user_records(user_id: int, db: Session = Depends(get_db)):

    records = db.query(Records).filter(Records.user_id == user_id).first()

    if records is None:
        raise HTTPException(status_code=404, detail="user has no records")
    return records
