from sqlalchemy import Column, Date, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.db_config.db_data import Base


class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True)
    title = Column(String)
    author = Column(String)
    published_date = Column(Date)
    borrowed_by_id = Column(Integer, ForeignKey("users.id"))
    borrowed_by = relationship("User", back_populates="borrowed_books")
