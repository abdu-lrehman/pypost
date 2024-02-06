from datetime import datetime, timedelta

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db_config.db_connect import get_db
from app.middleware.admin_dependency import admin_dependency
from app.middleware.user_dependency import user_dependency
from app.models.book import Book
from app.models.records import Records
from app.schemas.book_schema import BookCreate

router = APIRouter()


@router.get(
    "/user/get_book/{book_id}",
    response_model=BookCreate,
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
        db_book.status = "borrowed"
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
        db_book.status = "free"
        db.commit()
        db.refresh(db_book)

    return "book borrowed"


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
        content=book_data.content,
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
    books = db.query(Book).defer(Book.content).all()
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
