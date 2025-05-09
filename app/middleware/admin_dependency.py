import time

import jwt
from fastapi import Depends, FastAPI, HTTPException, Request, security
from fastapi.responses import JSONResponse
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.db_config.db_data import secretkey

app = FastAPI()
security = HTTPBearer()


def decode_jwt(token: str):
    try:
        decoded_token = jwt.decode(token, secretkey, algorithms=["HS256"])
        if decoded_token["userType"] == "admin":
            return decoded_token if decoded_token["exp"] >= time.time() else None
    except jwt.ExpiredSignatureError:
        return None
    except jwt.DecodeError:
        return None


def admin_dependency(
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> dict:
    token = credentials.credentials
    decoded_token = decode_jwt(token)
    if decoded_token is None:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    return decoded_token
