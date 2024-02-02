import os
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy.ext.declarative import declarative_base

env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

DATABASE_URL = os.getenv("DATABASE_URL")
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
callback = os.getenv("callback")
secretkey = os.getenv("SECRET_KEY")

Base = declarative_base()
