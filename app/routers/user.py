from fastapi import status, HTTPException, APIRouter, Depends
from .. import models, schemas, utils
from ..database import get_db
from sqlalchemy.orm import Session
from typing import List

router = APIRouter(
    prefix="/users",
    tags=['Users']
)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserResponse)
def add_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    hashed_password = utils.hash_password(user.password)
    user.password = hashed_password
    temp_user = models.User(**user.model_dump())
    db.add(temp_user)
    db.commit()
    db.refresh(temp_user)
    return temp_user

@router.get("/", response_model=List[schemas.UserResponse])
def read_posts(db: Session = Depends(get_db)):
    return db.query(models.User).all()


@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=schemas.UserResponse)
def get_post(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Requested user not found"
        )
    return user