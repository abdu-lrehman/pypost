import os
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy.ext.declarative import declarative_base

DATABASE_URL = os.environ.get("DATABASE_URL")
secretkey = os.environ.get("SECRET_KEY")
env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

# database_url = os.getenv("DATABASE_URL")
# secretkey = os.getenv("SECRET_KEY")

Base = declarative_base()
