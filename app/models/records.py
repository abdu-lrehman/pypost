from sqlalchemy import Column, DateTime, ForeignKey, Integer
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db_config.db_data import Base


class Records(Base):
    __tablename__ = "records"

    id = Column(Integer, primary_key=True)
    book_id = Column(Integer, ForeignKey("books.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    borrowed_at = Column(DateTime(timezone=True), default=func.now())

    book = relationship("Book", back_populates="records")
    user = relationship("User", back_populates="records")
