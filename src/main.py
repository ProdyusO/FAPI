from typing import List

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder

from crud import CRUD
import model
import schema

from db import SessionLocal, engine

model.Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post('/user/', response_model=schema.UserAdd)
def add_new_user(user: schema.UserAdd, db: Session = Depends(get_db)):
    username = jsonable_encoder(CRUD.get_user_by_username(db=db, username=user.username))
    if username:
        raise HTTPException(status_code=400, detail=f"User id {user.username} already exist: {username}")
    return jsonable_encoder(CRUD.add_user_details_to_db(db=db, user=user))


@app.get('/user/{user_id}', response_model=schema.User)
def get_user_by_id(id: int, db: Session = Depends(get_db)):
    user = jsonable_encoder(CRUD.get_user_by_id(db=db, id=id))
    return jsonable_encoder(user)


@app.put('/user/{user_id}', response_model=schema.User)
def update_user_details(id: int, update_param: schema.UpdateUser, db: Session = Depends(get_db)):
    details = jsonable_encoder(CRUD.get_user_by_id(db=db, id=id))
    if not details:
        raise HTTPException(status_code=404, detail=f"No record found to update")
    return jsonable_encoder(CRUD.update_user_details(db=db, details=update_param, id=id))


@app.patch('user/{user_id}', response_model=schema.User)
def patch_user_details(id: int, update_param: schema.PatchUser, db: Session = Depends(get_db)):
    details = jsonable_encoder(CRUD.get_user_by_id(db=db, id=id))
    if not details:
        raise HTTPException(status_code=404, detail=f"No record found to update")

    return jsonable_encoder(CRUD.patch_user_details(db=db, details=update_param, id=id))


@app.delete('/user/{user_id}')
def delete_user_by_id(id: int, db: Session = Depends(get_db)):
    details = jsonable_encoder(CRUD.get_user_by_id(db=db, id=id))
    if not details:
        raise HTTPException(status_code=404, detail=f"Not found ")

    try:
        jsonable_encoder(CRUD.delete_user_details_by_id(db=db, id=id))
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Unable to delete: {e}")
    return jsonable_encoder({"delete status": "success"})


@app.get('/user-list', response_model=List[schema.User])
def get_all_user_details(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = jsonable_encoder(CRUD.get_user(db=db, skip=skip, limit=limit))
    return users
