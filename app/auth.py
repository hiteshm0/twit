from fastapi import status, HTTPException, APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from . import models, schemas, utils
from .database import get_db
from sqlalchemy.orm import Session
from . import oauth2

router = APIRouter(
    tags=['Auth'],
    prefix="/login"
)

@router.post("/", response_model= schemas.Token)
def user_login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()

    if user is None:
        hashed_password = utils.hash_password("dummypassword")
    else: 
        hashed_password = user.password

    
    if not utils.verify_password(user_credentials.password, hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Credentials."
        )
    
    access_token = oauth2.create_token(data={"user_id": user.id})
    return {"access_token": access_token, "token_type": "bearer"}