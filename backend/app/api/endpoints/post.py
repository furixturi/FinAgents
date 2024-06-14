from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession
from app.db import get_session
from app.schemas import Post, PostCreate, PostUpdate
from app.crud import post as crud_post
from app.utils import validate_file_type
from typing import List, Optional
import os, shutil

router = APIRouter()

UPLOAD_FOLDER = "./uploads/"
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@router.post("/", response_model=Post)
async def create_post(
    title: str,
    content: str,
    user_id: int,
    file: UploadFile = File(...),
    session: AsyncSession = Depends(get_session),
):
    if not validate_file_type(file, ["image/jpeg", "image/png", "image/gif"]):
        raise HTTPException(
            status_code=400, detail="Only JPEG, PNG, and GIF images are allowed."
        )

    file_location = os.path.join(UPLOAD_FOLDER, file.filename)
    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    post_create = PostCreate(
        title=title, content=content, user_id=user_id, file_url=file_location
    )

    return await crud_post.create_post(session, post_create)


@router.get("/", response_model=list[Post])
async def get_posts(session: AsyncSession = Depends(get_session)):
    return await crud_post.get_posts(session)

@router.get("/{post_id}", response_model=Post)
async def get_post(post_id: int, session: AsyncSession = Depends(get_session)):
    return await crud_post.get_post(session, post_id)

@router.put("/{post_id}", response_model=Post)
async def update_post(
    post_id: int,
    title: Optional[str],
    content: Optional[str],
    file: UploadFile = None,
    session: AsyncSession = Depends(get_session),
):
    file_location = None
    if file:
        validate_file_type(file)
        file_location = os.path.join(UPLOAD_FOLDER, file.filename)
        with open(file_location, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    post_update = PostUpdate(title=title, content=content, file_url=file_location)
    return await crud_post.update_post(session, post_id, post_update)


@router.delete("/{post_id}")
async def delete_post(post_id: int, session: AsyncSession = Depends(get_session)):
    return await crud_post.delete_post(session, post_id)
