import os
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy.ext.declarative import declarative_base

# database_url = os.environ.get("DATABASE_URL")
# secretkey = os.environ.get("SECRET_KEY")

env_path = Path(__file__).resolve().parent.parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

database_url = os.getenv("DATABASE_URL")
print(database_url)
secretkey = os.getenv("SECRET_KEY")

Base = declarative_base()
