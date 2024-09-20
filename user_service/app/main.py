from fastapi import Depends, FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

from . import crud, schemas, models,database
from sqlalchemy.orm import Session


app = FastAPI()
models.Base.metadata.create_all(bind=database.engine)





@app.post("/users", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(database.get_db)):
    return crud.create_user(db=db, user=user)

@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(database.get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.get("/users", response_model=List[schemas.User])
def read_users(skip: int = 0, limit: int = 10, db: Session = Depends(database.get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users

@app.put("/users/{user_id}", response_model=schemas.User)
def update_user(user_id: int, user: schemas.UserCreate, db: Session = Depends(database.get_db)):
    db_user = crud.update_user(db, user_id=user_id, user=user)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@app.delete("/users/{user_id}", response_model=schemas.User)
def delete_user(user_id: int, db: Session = Depends(database.get_db)):
    db_user = crud.delete_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.get("/")
def read_root():
    return {"message": "User Service is running!"}
