from typing import List

from fastapi import APIRouter, Body, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db_config.db_connect import get_db
from app.models.user import User
from app.schemas.user_schema import UserCreate
from app.middleware.middleware import auth_middleware
from ..controllers.user_controller import (
    create_user,
    delete_user,
    get_all_users,
    get_user,
    update_user,
)

router = APIRouter()


@router.post("/users/register", response_model=UserCreate)
def create_user_route(user: UserCreate, db: Session = Depends(get_db)):
    return create_user(db=db, user=user)


@router.get(
    "/users/{user_id}",
    response_model=UserCreate,
    dependencies=[Depends(auth_middleware)],
)
def read_user_route(user_id: int, db: Session = Depends(get_db)):
    return get_user(db=db, user_id=user_id)


@router.get("/users/", dependencies=[Depends(auth_middleware)])
def read_all_users(db: Session = Depends(get_db)):
    return get_all_users(db)


@router.put(
    "/users/{user_id}",
    response_model=UserCreate,
    dependencies=[Depends(auth_middleware)],
)
def update_user_route(user_id: int, user: UserCreate, db: Session = Depends(get_db)):
    user_data = user.model_dump(exclude_unset=True)
    return update_user(db=db, user_id=user_id, user_data=user_data)


@router.delete("/users/{user_id}", dependencies=[Depends(auth_middleware)])
def delete_user_route(user_id: int, db: Session = Depends(get_db)):
    return delete_user(db=db, user_id=user_id)
