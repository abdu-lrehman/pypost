from pydantic import BaseModel
from datetime import date
from typing import Optional


class BookCreate(BaseModel):
    title: str
    author: str
    published_date: date
    borrowed_by_id: Optional[int] = None


class Book(BaseModel):
    id: int
    title: str
    author: str
    published_date: date
    borrowed_by_id: Optional[int] = None

    class Config:
        orm_mode = True
