from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from ..controllers.loginController import authenticate_user, create_access_token, authenticate_admin
from ..controllers.googleLoginController import oauth, get_google_user
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from ..dbconfig.dbconnect import get_db
from ..dbconfig.dbData import callback

router = APIRouter()


@router.post("/users/login")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(
        data={"sub": user.username, "id": user.id})
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/admins/login")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    admin = authenticate_admin(db, form_data.username, form_data.password)
    if not admin:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(
        data={"sub": admin.username, "id": admin.id})
    return {"access_token": access_token, "token_type": "bearer"}

# @router.post("/login/auth/google")
# async def login_via_google(request: Request):
#     redirect_uri = callback
#     print(redirect_uri)
#     return await oauth.google.authorize_redirect(request, redirect_uri)


# @router.get("/auth/callback")
# async def auth_callback(request: Request, db: Session = Depends(get_db)):
#     token = await oauth.google.authorize_access_token(request)
#     user_info = await get_google_user(token, db)

#     # You can handle the user_info as needed here
#     return {"user_info": user_info}
