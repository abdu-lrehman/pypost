from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from ..dbconfig.dbData import Base


class Book(Base):
    __tablename__ = 'books'

    id = Column(Integer, primary_key=True)
    title = Column(String)
    author = Column(String)
    published_date = Column(Date)
    borrowed_by_id = Column(Integer, ForeignKey('users.id'))
    borrowed_by = relationship('User', back_populates='borrowed_books')
