from sqlalchemy import Column, Integer, String

from app.db_config.db_data import Base


class Admin(Base):
    __tablename__ = "admins"

    id = Column(Integer, primary_key=True)
    username = Column(String)
    email = Column(String)
    password = Column(String)
