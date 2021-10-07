from sqlalchemy import Column, Integer, String
from db import Base


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    email = Column(String(255), unique=True)
    password = Column(String(100))
    register_date = Column(String(100))
