from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db import get_session
from app.schemas import Post, PostCreate, PostUpdate
from app.crud import post as crud_post

router = APIRouter()

@router.post("/", response_model=Post)
async def create_post(post_create: PostCreate, session: AsyncSession = Depends(get_session)):
    return await crud_post.create_post(session, post_create)

@router.get("/", response_model=list[Post])
async def get_posts(session: AsyncSession = Depends(get_session)):
    return await crud_post.get_posts(session)

@router.put("/{post_id}", response_model=Post)
async def update_post(post_id: int, post_update: PostUpdate, session: AsyncSession = Depends(get_session)):
    return await crud_post.update_post(session, post_id, post_update)

@router.delete("/{post_id}")
async def delete_post(post_id: int, session: AsyncSession = Depends(get_session)):
    return await crud_post.delete_post(session, post_id)