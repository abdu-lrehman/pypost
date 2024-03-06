from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from app.db_config.db_connect import get_db
from app.middleware.user_dependency import user_dependency
from app.models.records import Records
from app.models.user import User
from app.schemas.user_schema import UserCreate

router = APIRouter()


def __hash_password(password: str):
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    return pwd_context.hash(password)


@router.post("/", response_model=UserCreate)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    hashed_password = __hash_password(user.password)

    user_data = user.model_dump(exclude={"password"})
    db_user = User(**user_data, password=hashed_password)

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user


@router.put("/{user_id}", response_model=UserCreate)
def update_user(
    user: UserCreate,
    db: Session = Depends(get_db),
    decoded_token: dict = Depends(user_dependency),
):
    user_data = user.model_dump(exclude_unset=True)
    user_id = decoded_token["id"]
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:

        raise HTTPException(status_code=404, detail="User not found")

    if "password" in user_data:
        user_data["password"] = __hash_password(user_data["password"])

    for field, value in user_data.items():
        setattr(user, field, value)

    db.commit()
    db.refresh(user)

    return user


@router.delete("/{user_id}", dependencies=[Depends(user_dependency)])
def delete_user(
    decoded_token: dict = Depends(user_dependency), db: Session = Depends(get_db)
):
    user_id = decoded_token["id"]
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:

        raise HTTPException(status_code=404, detail="User not found")

    db.delete(user)
    db.commit()

    return JSONResponse(content="User deleted successfully")


@router.get("/")
def get_user_details(
    db: Session = Depends(get_db),
    decoded_token: dict = Depends(user_dependency),
):
    user_id = decoded_token["id"]
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:

        raise HTTPException(status_code=404, detail="user not found")

    return user


@router.get("/record")
def get_user_records(
    db: Session = Depends(get_db), decoded_token: dict = Depends(user_dependency)
):
    user_id = decoded_token["id"]
    records = db.query(Records).filter(Records.user_id == user_id).first()
    if records is None:

        raise HTTPException(status_code=404, detail="user has no records")

    return records
