from typing import List
from fastapi import Depends, HTTPException, status, APIRouter
from sqlalchemy import func
from sqlalchemy.orm import Session
from .. import models, schemas, oauth2
from ..database import get_db

router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)

@router.get("/", response_model=List[schemas.PostOut])
def read_posts(db: Session = Depends(get_db), limit:int = 10, offset:int = 0):
    #return db.query(models.Post).limit(limit).offset(offset).all()

    temp_query = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).limit(limit).offset(offset)
    posts = temp_query.all()

    return posts

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.PostReturn)
def add_post(post: schemas.Post, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    temp_post = models.Post(**post.model_dump())
    temp_post.user_id = current_user.id
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
def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    query = db.query(models.Post).filter(models.Post.id == id)
    post = query.first()

    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail = "Requested post not found"
        )
    
    if( post.user_id != current_user.id): 
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not own the post."
        )
    
    query.delete()
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