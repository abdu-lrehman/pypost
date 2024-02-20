from typing import Optional

from pydantic import BaseModel, EmailStr, constr, validator


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str = None
