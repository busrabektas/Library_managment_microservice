# user_service/main.py

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from typing import List

from . import crud, schemas, models, database
from .producer import send_user_event
import logging

app = FastAPI()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

models.Base.metadata.create_all(bind=database.engine)


def get_db_session():
    db_gen = database.get_db()
    return next(db_gen)

@app.post("/users", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db_session)):
    created_user = crud.create_user(db=db, user=user)
    send_user_event('USER_CREATED', schemas.User.model_validate(created_user).model_dump())
    logger.info(f"User created: {created_user}")
    return created_user

@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db_session)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@app.get("/users", response_model=List[schemas.User])
def read_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db_session)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users

@app.put("/users/{user_id}", response_model=schemas.User)
def update_user(user_id: int, user: schemas.UserCreate, db: Session = Depends(get_db_session)):
    updated_user = crud.update_user(db=db, user_id=user_id, user=user)
    if updated_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    send_user_event('USER_UPDATED', schemas.User.model_validate(updated_user).model_dump())
    logger.info(f"User updated: {updated_user}")
    return updated_user

@app.delete("/users/{user_id}", response_model=schemas.User)
def delete_user(user_id: int, db: Session = Depends(get_db_session)):
    deleted_user = crud.delete_user(db=db, user_id=user_id)
    if deleted_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    send_user_event('USER_DELETED', {'id': user_id})
    logger.info(f"User deleted: {deleted_user}")
    return deleted_user

@app.get("/")
def read_root():
    return {"message": "User Service is running!"}
