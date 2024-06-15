from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db import get_session
from app.schemas import User, UserCreate, UserUpdate
from app.crud import user as crud_user
from typing import List

router = APIRouter()

@router.post("/", response_model=User)
async def create_user(user_create: UserCreate, session: AsyncSession = Depends(get_session)):
    return await crud_user.create_user(session, user_create)

@router.get("/", response_model=List[User])
async def get_users(session: AsyncSession = Depends(get_session)):
    return await crud_user.get_users(session)

@router.get("/{user_id}", response_model=User)
async def get_user(user_id: int, session: AsyncSession = Depends(get_session)):
    return await crud_user.get_user_by_id(session, user_id)

@router.put("/{user_id}", response_model=User)
async def update_user(user_id: int, user_update: UserUpdate, session: AsyncSession = Depends(get_session)):
    return await crud_user.update_user(session, user_id, user_update)

@router.delete("/{user_id}", response_model=User)
async def delete_user(user_id: int, session: AsyncSession = Depends(get_session)):
    return await crud_user.delete_user(session, user_id)