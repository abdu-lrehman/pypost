from sqlalchemy import Column, Date, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.db_config.db_data import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String)
    email = Column(String)
    password = Column(String)
    borrowed_books = relationship("Book", back_populates="borrowed_by")
    records = relationship("Records", back_populates="user")
