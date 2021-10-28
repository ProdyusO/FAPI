import datetime
import schema

from model import users
from db import database


class CRUD:
    async def get_user_by_username(username: str):
        return await database.fetch_one(users.select().where(users.c.username == username))

    async def get_user_by_id(id: int):
        return await database.fetch_one(users.select().where(users.c.id == id))

    async def get_users(skip: int, limit: int):
        return await database.fetch_all(query=users.select().offset(skip).limit(limit))

    async def add_user_details_to_db(details: schema.UserAdd):
        password = details.password + 'hesh123tgghhhyy9877'
        register_date = datetime.datetime.now()
        detail = users.insert().values(
            username=details.username,
            email=details.email,
            password=password,
            register_date=register_date
        )
        await database.execute(detail)
        return schema.UserBase(**details.dict())

    async def update_user_details(id: int, details: schema.UserBase):
        password = details.password + 'heshff34749191'
        user = users.update().where(users.c.id == id).values(
            username=details.username,
            email=details.email,
            password=password
        )
        await database.execute(user)
        return schema.UserBase(**details.dict())

    async def patch_user_details(id: int, details: schema.PatchUser):
        password = details.password + 'heshgglkl3435656'
        user = users.update().where(users.c.id == id).values(password=password)
        await database.execute(user)
        return schema.PatchUser(**(details.dict()))

    async def delete_user_details_by_id(id: int):
        try:
            detail = users.delete().where(id == users.c.id)
            await database.execute(detail)
        except Exception as e:
            raise Exception(e)
