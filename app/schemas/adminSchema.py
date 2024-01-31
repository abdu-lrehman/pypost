from pydantic import BaseModel, EmailStr, constr, validator
from typing import Optional


class AdminCreate(BaseModel):
    username: str
    email: EmailStr
    password: constr(min_length=8) = None
