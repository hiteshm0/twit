from pydantic import BaseModel, EmailStr

class Post(BaseModel):
    title: str
    content: str
    published: bool = True

class BaseUser(BaseModel):
    username: str
    email: EmailStr

class UserCreate(BaseUser):
    password: str

class UserResponse(BaseUser):
    id: int