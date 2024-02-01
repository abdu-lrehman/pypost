from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
import jwt
import time
from fastapi.security import HTTPBearer
from ..dbconfig.dbData import secretkey

app = FastAPI()
security = HTTPBearer()


def decode_jwt(token: str):
    try:
        decoded_token = jwt.decode(token, secretkey, algorithms=["HS256"])
        return decoded_token if decoded_token["exp"] >= time.time() else None
    except jwt.ExpiredSignatureError:
        return None  # Token is expired
    except jwt.DecodeError:
        return None  # Invalid token


@app.middleware("http")
async def auth_middleware(request: Request, call_next):
    """
    Middleware for authentication.
    It checks the token for protected routes.
    """
    path = request.url.path

    # List of routes that don't require authentication
    non_auth_routes = [
        "/users/login",
        "/admins/login",
        "/users/register",
        "/admins/register",
    ]

    if path not in non_auth_routes:
        authorization: str = request.headers.get("Authorization")
        if authorization:
            schema, _, token = authorization.partition(" ")
            if schema and token and schema.lower() == "bearer":
                token_data = decode_jwt(token)
                if token_data:
                    # If needed, you can attach basic token data to request state
                    request.state.user_info = token_data
                else:
                    # Respond with an error if the token is invalid or expired
                    return JSONResponse(
                        content={"error": "Invalid or expired token"}, status_code=401
                    )
        else:
            # Respond with an error if no token is provided in a protected route
            return JSONResponse(
                content={"error": "Authorization token is required"}, status_code=401
            )

    # Proceed to the next middleware or route handler if authentication passes
    response = await call_next(request)
    return response


# Define your endpoint routes here...
