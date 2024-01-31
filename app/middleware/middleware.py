from fastapi import FastAPI, Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from ..dbconfig.dbconnect import get_db  # Ensure the correct relative import
import time
from ..models.user import User
from ..controllers.loginController import get_user, get_admin
from ..dbconfig.dbData import secretkey


app = FastAPI()
security = HTTPBearer()


def decode_jwt(token: str):
    try:
        decoded_token = jwt.decode(token, secretkey, algorithms=["HS256"])
        return decoded_token if decoded_token['exp'] >= time.time() else None
    except jwt.ExpiredSignatureError:
        return None  # Token is expired
    except jwt.DecodeError:
        return None  # Invalid token


@app.middleware("http")
async def db_session_middleware(request: Request, call_next):
    # Create a new db session and store it in request state
    request.state.db = next(get_db())
    response = await call_next(request)
    # request.state["db"] = next(get_db())
    print(request.state.db)
    # request.state.db.close()  # Close the db session
    return response


@app.middleware("http")
async def auth_middleware(request: Request, call_next):
    path = request.url.path

    # List of routes that don't require authentication
    non_auth_routes = ["/users/login", "/admins/login",
                       "/users/register", "/admins/register"]

    if path not in non_auth_routes:
        token = request.headers.get("Authorization")
        if token:
            token = token.split(" ")[1]  # Assuming Bearer token
            token_data = decode_jwt(token)
            if token_data:
                # Use request.state.db for database operations
                request.state.user = get_user(
                    token_data['sub'], request.state.db)
            else:
                return JSONResponse(content={"error": "Invalid or expired token"}, status_code=401)

    response = await call_next(request)
    return response

# Define your endpoint routes here...
