from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from .dbData import Base
from ..models.user import User
from ..models.book import Book
from .dbData import DATABASE_URL

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def dbconnect():
    try:

        # Attempt to connect to the database
        with engine.connect() as connection:
            # If this point is reached, the connection is successful
            print("Database connection established.")
            Base.metadata.create_all(engine)

    except SQLAlchemyError as e:
        # Handle the error if the connection fails
        print("Error occurred during database connection:", str(e))


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db
