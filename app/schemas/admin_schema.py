from pydantic import BaseModel, EmailStr, constr, validator


class AdminCreate(BaseModel):
    username: str
    email: EmailStr
    password: constr(min_length=8) = None
