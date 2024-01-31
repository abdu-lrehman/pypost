from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.orm import Session
from typing import List
from ..dbconfig.dbconnect import get_db
from ..models.user import User
from ..schemas.bookSchema import BookCreate
from ..controllers.bookController import create_book, get_book, update_book, delete_book, get_all_books
router = APIRouter()


@router.post("/books/", response_model=BookCreate)
def create_book_route(book: BookCreate, db: Session = Depends(get_db)):
    return create_book(db=db, book_data=book)


@router.get("/books/{book_id}", response_model=BookCreate)
def read_book_route(book_id: int, db: Session = Depends(get_db)):
    return get_book(db=db, book_id=book_id)


@router.get("/books/")
def read_all_books(db: Session = Depends(get_db)):
    return get_all_books(db)


@router.put("/books/{book_id}", response_model=BookCreate)
def update_book_route(book_id: int, book: BookCreate, db: Session = Depends(get_db)):
    return update_book(db=db, book_id=book_id, updated_data=book)


@router.delete("/books/{book_id}")
def delete_user_route(book_id: int, db: Session = Depends(get_db)):
    return delete_book(db=db, book_id=book_id)
