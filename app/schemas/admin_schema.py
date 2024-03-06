from typing import Optional

from pydantic import BaseModel, EmailStr


class AdminCreate(BaseModel):
    username: str
    email: EmailStr
    password: Optional[str] = None
