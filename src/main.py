from fastapi import FastAPI, HTTPException, APIRouter
from db import database, metadata, engine
from typing import List

from services import CRUD
import schema


metadata.create_all(bind=engine)

app = FastAPI()
#router = APIRouter()


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


@app.post('/user/', response_model=schema.UserBase)
async def add_new_user(user: schema.UserBase):
    detail = await CRUD.get_user_by_username(username=user.username)
    if detail is not None:
        raise HTTPException(status_code=400, detail=f"User with name {user.username} already exist")
    return await CRUD.add_user_details_to_db(details=user)


@app.get('/user/{user_id}/', response_model=schema.UserAdd)
async def get_user_by_id(id: int):
    user = await CRUD.get_user_by_id(id=id)
    if not user:
        raise HTTPException(status_code=400, detail=f'User with id: {id} not found')
    return user


@app.put('/user/{user_id}', response_model=schema.UserBase)
async def update_user_details(id: int, update_param: schema.UserBase):
    details = await CRUD.get_user_by_id(id=id)
    if not details:
        raise HTTPException(status_code=404, detail=f"No record found to update")
    return await CRUD.update_user_details(details=update_param, id=id)


@app.patch('/user/{user_id}', response_model=schema.PatchUser)
async def change_password(id: int, update_param: schema.PatchUser):
    details = await CRUD.get_user_by_id(id=id)
    if not details:
        raise HTTPException(status_code=404, detail=f"No record found to update")
    return await CRUD.patch_user_details(details=update_param, id=id)


@app.delete('/user/{user_id}/')
async def delete_user_by_id(id: int):
    details = await CRUD.get_user_by_id(id=id)
    if not details:
        raise HTTPException(status_code=404, detail=f"Not found ")
    try:
        await CRUD.delete_user_details_by_id(id=id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Unable to delete: {e}")
    return {"delete status": "success"}


@app.get('/user-list', response_model=List[schema.UserAdd])
async def get_all_users_details(skip: int = 0, limit: int = 100):
    users = await CRUD.get_users(skip=skip, limit=limit)
    if not users:
        raise HTTPException(status_code=400, detail='Base is empty')
    return users
