from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.orm import Session
from typing import List
from ..dbconfig.dbconnect import get_db
from ..models.user import User
from ..schemas.userSchema import UserCreate

from ..controllers.userController import create_user, get_user, update_user, delete_user, get_all_users

router = APIRouter()


@router.post("/users/register", response_model=UserCreate)
def create_user_route(user: UserCreate, db: Session = Depends(get_db)):
    return create_user(db=db, user=user)


@router.get("/users/{user_id}", response_model=UserCreate)
def read_user_route(user_id: int, db: Session = Depends(get_db)):
    return get_user(db=db, user_id=user_id)


@router.get("/users/")
def read_all_users(db: Session = Depends(get_db)):
    return get_all_users(db)


@router.put("/users/{user_id}", response_model=UserCreate)
def update_user_route(user_id: int, user: UserCreate, db: Session = Depends(get_db)):
    user_data = user.model_dump(exclude_unset=True)
    return update_user(db=db, user_id=user_id, user_data=user_data)


@router.delete("/users/{user_id}")
def delete_user_route(user_id: int, db: Session = Depends(get_db)):
    return delete_user(db=db, user_id=user_id)
