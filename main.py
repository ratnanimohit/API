from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

import models
import schemas
import crud
from database import engine, get_db

# Create all database tables on startup
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="User Management API",
    description="A simple CRUD API for managing users",
    version="1.0.0"
)

from fastapi.responses import RedirectResponse

@app.get("/", include_in_schema=False)
def root():
    return RedirectResponse(url="/docs")

@app.post("/users", response_model=schemas.User, status_code=status.HTTP_201_CREATED)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    """
    Create a new user.
    """
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered"
        )
    created_user = crud.create_user(db=db, user=user)
    if not created_user:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Could not create user"
        )
    return created_user

@app.get("/users", response_model=List[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Get all users.
    """
    users = crud.get_users(db, skip=skip, limit=limit)
    return users

@app.get("/users/{id}", response_model=schemas.User)
def read_user(id: int, db: Session = Depends(get_db)):
    """
    Get a single user by ID.
    """
    db_user = crud.get_user(db, user_id=id)
    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return db_user

@app.put("/users/{id}", response_model=schemas.User)
def update_user(id: int, user: schemas.UserUpdate, db: Session = Depends(get_db)):
    """
    Update an existing user.
    """
    db_user = crud.get_user(db, user_id=id)
    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Check if email is being updated to an existing email
    if user.email != db_user.email:
        existing_user = crud.get_user_by_email(db, email=user.email)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Email already registered"
            )
            
    updated_user = crud.update_user(db=db, user_id=id, user=user)
    return updated_user

@app.delete("/users/{id}", status_code=status.HTTP_200_OK)
def delete_user(id: int, db: Session = Depends(get_db)):
    """
    Delete a user.
    """
    db_user = crud.get_user(db, user_id=id)
    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    crud.delete_user(db=db, user_id=id)
    return {"message": "User deleted successfully"}
