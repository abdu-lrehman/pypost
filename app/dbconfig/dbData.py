from sqlalchemy.ext.declarative import declarative_base
from dotenv import load_dotenv
import os
from pathlib import Path

# Calculate the path to the .env file
env_path = Path(__file__).resolve().parent.parent.parent / '.env'

# Load the .env file
load_dotenv(dotenv_path=env_path)

DATABASE_URL = os.getenv("DATABASE_URL")
SECRET_KEY = os.getenv("SECRET_KEY")
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
callback = os.getenv("callback")
secretkey = os.getenv("SECRET_KEY")

Base = declarative_base()
