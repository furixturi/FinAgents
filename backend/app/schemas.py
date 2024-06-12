from pydantic import BaseModel
from typing import List

class UserBase(BaseModel):
    name: str
    email: str

class UserCreate(UserBase):
    pass

class UserUpdate(BaseModel):
    email: str

class User(UserBase):
    id: int
    posts: List["Post"] = []

    class Config:
        orm_mode = True

class PostBase(BaseModel):
    title: str
    content: str

class PostCreate(PostBase):
    user_id: int

class PostUpdate(PostBase):
    pass

class Post(PostBase):
    id: int
    user_id: int
    author: User

    class Config:
        orm_mode = True
