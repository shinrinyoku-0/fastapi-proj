from pydantic import BaseModel, EmailStr, conint
from datetime import datetime
from typing import Optional

class User(BaseModel):
    email: EmailStr
    id: int
    created_at: datetime

    class Config:
        orm_mode: True

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

class PostCreate(PostBase):
    pass

class Post(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: User


class PostOut(BaseModel):
    Post: Post
    votes: int

    class Config:
        orm_mode: True

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserOut(User):
    
    class Config:
        orm_mode: True

class UserLogin(UserCreate):
    pass

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str]

class Vote(BaseModel):
    post_id: int
    dir: conint(ge=0, le=1)