from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.user import User
from ..schemas.userSchema import UserCreate
from passlib.context import CryptContext

# Configuration for Passlib
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str):
    return pwd_context.hash(password)


def create_user(db: Session, user: UserCreate):
    hashed_password = hash_password(user.password)

    user_data = user.model_dump(exclude={"password"})
    db_user = User(**user_data, password=hashed_password)

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user


def update_user(db: Session, user_id: int, user_data: dict):
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    if "password" in user_data:
        user_data["password"] = hash_password(user_data["password"])

    for field, value in user_data.items():
        setattr(user, field, value)

    db.commit()
    db.refresh(user)
    return user


def delete_user(db: Session, user_id: int):
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    db.delete(user)
    db.commit()
    return {"message": "User deleted successfully"}


def get_all_users(db: Session):
    users = db.query(User).all()
    return users


def get_user(db: Session, user_id: int):

    user = db.query(User).filter(User.id == user_id).first()

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user
