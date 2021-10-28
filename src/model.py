from sqlalchemy import Column, Integer, Table, String
from db import metadata

users = Table(
    'users',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('username', String(100), unique=True),
    Column('email', String(100), unique=True),
    Column('password', String(100)),
    Column('register_date', String(100))
)
