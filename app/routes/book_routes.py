from typing import List

from fastapi import APIRouter, Body, Depends, HTTPException
from sqlalchemy.orm import Session
from app.middleware.middleware import auth_middleware

from app.controllers.book_controller import (create_book, delete_book,
                                             get_all_books, get_book,
                                             update_book)
from app.db_config.db_connect import get_db
from app.models.user import User
from app.schemas.book_schema import BookCreate

router = APIRouter()


@router.post("/books/", response_model=BookCreate, dependencies=[Depends(auth_middleware)])
def create_book_route(book: BookCreate, db: Session = Depends(get_db)):
    return create_book(db=db, book_data=book)


@router.get("/books/{book_id}", response_model=BookCreate, dependencies=[Depends(auth_middleware)])
def read_book_route(book_id: int, db: Session = Depends(get_db)):
    return get_book(db=db, book_id=book_id)


@router.get("/books/", dependencies=[Depends(auth_middleware)])
def read_all_books(db: Session = Depends(get_db)):
    return get_all_books(db)


@router.put("/books/{book_id}", response_model=BookCreate, dependencies=[Depends(auth_middleware)])
def update_book_route(book_id: int, book: BookCreate, db: Session = Depends(get_db)):
    return update_book(db=db, book_id=book_id, updated_data=book)


@router.delete("/books/{book_id}", dependencies=[Depends(auth_middleware)])
def delete_user_route(book_id: int, db: Session = Depends(get_db)):
    return delete_book(db=db, book_id=book_id)
