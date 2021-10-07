from typing import Optional
from pydantic import BaseModel
from datetime import date


class UserBase(BaseModel):
    username: str
    email: str
    password: str
    register_date: date


class UserAdd(UserBase):
    username: Optional[str] = None

    class Config:
        orm_mode = True


class User(UserAdd):
    id: int

    class Config:
        orm_mode = True


class UpdateUser(BaseModel):
    id: int
    username: Optional[str] = None
    email: str
    password: str
    register_date: date

    class Config:
        orm_mode = True


class PatchUser(BaseModel):
    password: str

    class Config:
        orm_mode = True
