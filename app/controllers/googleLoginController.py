from fastapi import HTTPException, status, Depends
from sqlalchemy.orm import Session
from authlib.integrations.starlette_client import OAuth
from ..dbconfig.dbData import SECRET_KEY, GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET
from ..models.user import User
from ..controllers.loginController import create_access_token
import requests

oauth = OAuth()
oauth.register(
    name='google',
    client_id=GOOGLE_CLIENT_ID,
    client_secret=GOOGLE_CLIENT_SECRET,
    access_token_url='https://accounts.google.com/o/oauth2/token',
    access_token_params=None,
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    authorize_params=None,
    api_base_url='https://www.googleapis.com/oauth2/v1/',
    client_kwargs={'scope': 'openid email profile'},
)


def get_google_userinfo(access_token):
    response = requests.get(
        'https://www.googleapis.com/oauth2/v3/userinfo',
        headers={'Authorization': f'Bearer {access_token}'}
    )
    return response.json()


async def get_google_user(token, db: Session):

    user_info = get_google_userinfo(token['access_token'])
    user_info = token['userinfo']  # Example, actual key may vary

    google_id = user_info['id']
    email = user_info['email']
    print("hello")
    # Check if user exists
    user = db.query(User).filter(User.google_id == google_id).first()

    if not user:
        # Create new user if doesn't exist
        user_data = {
            "username": email,  # or any other unique identifier
            "googleId": google_id,
            "email": email,
            # You can add more fields here if your User model has them
            # For example, "name": name, if you have a name field
        }
        user = User(**user_data)
        db.add(user)
        db.commit()
        db.refresh(user)

    # Generate JWT token
    access_token = create_access_token(
        data={"sub": user.username, "userId": user.id})
    return access_token
