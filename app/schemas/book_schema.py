from datetime import date
from typing import Optional

from pydantic import BaseModel


class BookCreate(BaseModel):
    title: str
    author: str
    published_date: date
    borrowed_by_id: Optional[int] = None
