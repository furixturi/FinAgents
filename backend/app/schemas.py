from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

# User
class UserBase(BaseModel):
    name: str
    email: str

class UserCreate(UserBase):
    pass

class UserUpdate(BaseModel):
    name: str
    email: str

class User(UserBase):
    id: int

    class Config:
        orm_mode = True

# Post
class PostBase(BaseModel):
    title: str
    content: str
    file_url: Optional[str] = None

class PostCreate(PostBase):
    user_id: int

class PostUpdate(PostBase):
    pass

class Post(PostBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True

# ChatMessage
class ChatMessageBase(BaseModel):
    message: str
    
class ChatMessageCreate(ChatMessageBase):
    user_id: int
    
class ChatMessage(ChatMessageBase):
    id: int
    timestamp: datetime
    
    class Config:
        orm_mode = True