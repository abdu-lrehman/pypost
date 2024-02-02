from typing import Optional

from pydantic import BaseModel, EmailStr, constr, validator


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: constr(min_length=8) = None
