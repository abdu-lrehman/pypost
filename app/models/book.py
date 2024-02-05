from datetime import datetime

from sqlalchemy import Column, Date, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db_config.db_data import Base


class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True)
    title = Column(String)
    author = Column(String)
    content = Column(String)
    published_date = Column(Date)
    borrowed_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    borrowed_by_id = Column(Integer, ForeignKey("users.id"))

    borrowed_by = relationship("User", back_populates="borrowed_books")
    records = relationship("Records", back_populates="book")
