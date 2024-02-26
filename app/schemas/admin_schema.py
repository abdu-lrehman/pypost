from pydantic import BaseModel, EmailStr
from typing import Optional


class AdminCreate(BaseModel):
    username: str
    email: EmailStr
    password: Optional[str] = None
