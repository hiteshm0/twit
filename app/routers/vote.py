from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session

from .. import oauth2, schemas, models
from ..database import get_db

router = APIRouter(
    prefix="/votes",
    tags=['Votes']
)

@router.post("/")
def make_vote(vote: schemas.MakePost, current_user: int = Depends(oauth2.get_current_user), db: Session = Depends(get_db)):
    find_post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()
    if find_post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Requested Post Not Found.')
    
    temp_query = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id, models.Vote.user_id == current_user.id)
    temp_post = temp_query.first()
    
    if vote.direction > 0:
        if temp_post is not None:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Vote already exists"
            )
        
        temp_vote = models.Vote(user_id = current_user.id, post_id = vote.post_id)
        db.add(temp_vote)
        db.commit()
        db.refresh(temp_vote)
        return {"Message" : "Vote added successfully"}
    
    else:
        if temp_post is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Vote does not exist to remove."
            )
        
        temp_query.delete()
        db.commit()

        return None

    