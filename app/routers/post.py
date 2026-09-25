from fastapi import Depends, HTTPException, status, APIRouter
from sqlalchemy.orm import Session
from .. import models, schemas
from ..database import get_db

router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)

@router.get("/")
def read_posts(db: Session = Depends(get_db)):
    return db.query(models.Post).all()

@router.post("/", status_code=status.HTTP_201_CREATED)
def add_post(post: schemas.Post, db: Session = Depends(get_db)):
    temp_post = models.Post(**post.model_dump())
    db.add(temp_post)
    db.commit()
    db.refresh(temp_post)
    return temp_post

@router.get("/{id}", status_code=status.HTTP_200_OK)
def get_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Requested post not found"
        )
    return post

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id)

    if post.first() is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail = "Requested post not found"
        )
    
    post.delete()
    db.commit()
    return None

@router.put("/{id}")
def update_post(id: int, post: schemas.Post, db: Session = Depends(get_db)):
    query = db.query(models.Post).filter(models.Post.id == id)
    temp_post = query.first()

    if temp_post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail = "Requested post not found"
        )
    
    query.update(post.model_dump())
    db.commit()
    db.refresh(temp_post)
    return temp_post