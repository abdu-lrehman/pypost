import datetime

import jwt
from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from app.db_config.db_connect import get_db
from app.db_config.db_data import secretkey
from app.models.admin import Admin
from app.models.user import User

router = APIRouter()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_user(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()


def get_admin(db: Session, username: str):
    return db.query(Admin).filter(Admin.username == username).first()


def authenticate_user(db: Session, username: str, password: str):
    user = get_user(db, username)
    if not user or not verify_password(password, user.password):
        return False
    return user


def authenticate_admin(db: Session, username: str, password: str):
    admin = get_admin(db, username)
    if not admin or not verify_password(password, admin.password):
        return False
    return admin


def create_access_token(data: dict):
    expiration = datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    to_encode = data.copy()
    to_encode["exp"] = expiration
    encoded_jwt = jwt.encode(to_encode, secretkey, algorithm="HS256")
    return encoded_jwt


router = APIRouter()


@router.post("/user/login")
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(
        data={"sub": user.username, "id": user.id, "userType": "user"}
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/admin/login")
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    admin = authenticate_admin(db, form_data.username, form_data.password)
    if not admin:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(
        data={"sub": admin.username, "id": admin.id, "userType": "admin"}
    )
    return {"access_token": access_token, "token_type": "bearer"}
