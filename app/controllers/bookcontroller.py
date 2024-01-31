from fastapi import HTTPException
from sqlalchemy.orm import Session
from ..models.user import User
from ..models.book import Book
from ..schemas.bookSchema import BookCreate


def create_book(db: Session, book_data: BookCreate):
    db_book = Book(title=book_data.title,
                   author=book_data.author,
                   published_date=book_data.published_date,
                   borrowed_by_id=book_data.borrowed_by_id)

    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book

# Get a book by ID


def get_book(db: Session, book_id: int):
    return db.query(Book).filter(Book.id == book_id).first()


# Update a user's details
def update_book(db: Session, book_id: int, updated_data):
    db_book = db.query(Book).filter(Book.id == book_id).first()
    if db_book:
        db_book.title = updated_data.title
        db_book.author = updated_data.author
        db_book.published_date = updated_data.published_date
        db_book.borrowed_by_id = updated_data.borrowed_by_id
        db.commit()
        db.refresh(db_book)
    return db_book


# Delete a book
def delete_book(db: Session, book_id: int):
    db_book = db.query(Book).filter(Book.id == book_id).first()
    if db_book:
        db.delete(db_book)
        db.commit()
    return db_book


def get_all_books(db: Session):
    books = db.query(Book).all()
    return books
