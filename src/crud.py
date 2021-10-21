from sqlalchemy.orm import Session
import model
import schema


class CRUD:
    def get_user_by_username(db: Session, username: str):
        return db.query(model.User).filter(model.User.username == username).first()


    def get_user_by_id(db: Session, id: int):
        return db.query(model.User).filter(model.User.id == id).first()


    def get_user(db: Session, skip: int = 0, limit: int = 100):
        return db.query(model.User).offset(skip).limit(limit).all()


    def add_user_details_to_db(db: Session, user: schema.UserAdd):
        details = model.User(
            username=user.username,
            email=user.email,
            password=user.password,
            register_date=user.register_date,
        )
        db.add(details)
        db.commit()
        db.refresh(details)
        return model.User(**user.dict())


    def update_user_details(db: Session, id: int, details: schema.UpdateUser):
        db.query(model.User).filter(model.User.id == id).update(vars(details))
        db.commit()
        return db.query(model.User).filter(model.User.id == id).first()


    def patch_user_details(db: Session, id: int, details: schema.PatchUser):
        db.query(model.User).filter(model.User.id == id).update(vars(details))
        db.commit()
        return db.query(model.User).filter(model.User.id == id).first()


    def delete_user_details_by_id(db: Session, id: int):
        try:
            db.query(model.User).filter(model.User.id == id).delete()
            db.commit()
        except Exception as e:
            raise Exception(e)
