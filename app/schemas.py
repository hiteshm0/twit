from pydantic import BaseModel, EmailStr, ConfigDict, Field
from datetime import datetime
from typing import Optional


class BaseUser(BaseModel):
    username: str
    email: EmailStr

class Post(BaseModel):
    title: str
    content: str
    published: bool = True

class PostReturn(Post):
    id: int
    created_by: BaseUser = Field(validation_alias="owner")
class UserCreate(BaseUser):
    password: str

class UserResponse(BaseUser):
    user_id: int = Field(validation_alias="id")
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=False,
        populate_by_name=False
    )


class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional['int'] = None