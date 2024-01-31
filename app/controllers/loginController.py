from sqlalchemy.orm import Session
from passlib.context import CryptContext
import jwt
from app.models.user import User
from app.models.admin import Admin
from ..dbconfig.dbData import secretkey
import datetime

# Configuration for Passlib
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
    # Set the expiration time for the token (e.g., 1 hour from now)
    expiration = datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    to_encode = data.copy()
    to_encode['exp'] = expiration
    encoded_jwt = jwt.encode(to_encode, secretkey, algorithm="HS256")
    return encoded_jwt
