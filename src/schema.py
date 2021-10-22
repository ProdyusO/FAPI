from pydantic import BaseModel


class UserBase(BaseModel):
    username: str
    email: str
    password: str


class UserAdd(UserBase):
    id: int
    register_date: str

    class Config:
        orm_mode = True


class PatchUser(BaseModel):
    password: str

    class Config:
        orm_mode = True
