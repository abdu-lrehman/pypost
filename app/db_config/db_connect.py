from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import sessionmaker
from app.db_config.db_data import DATABASE_URL, Base
from app.models.book import Book
from app.models.user import User

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def dbconnect():
    try:

        with engine.connect() as connection:
            print("Database connection established.")
            Base.metadata.create_all(engine)

    except SQLAlchemyError as e:
        print("Error occurred during database connection:", str(e))


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db
