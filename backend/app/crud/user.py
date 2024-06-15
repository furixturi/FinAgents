from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from app.schemas import UserCreate, UserUpdate
from app.models import User
from fastapi import HTTPException


async def create_user(session: AsyncSession, user_create: UserCreate):
    user = User(name=user_create.name, email=user_create.email)
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user


async def get_users(session: AsyncSession):
    result = await session.execute(select(User))
    users = result.scalars().all()
    return users


async def get_user_by_id(session, user_id):
    result = await session.execute(select(User).filter_by(id=user_id))
    user = result.scalar_one_or_none()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


async def update_user(session, user_id, user_update):
    result = await session.execute(select(User).filter_by(id=user_id))
    user = result.scalar_one_or_none()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    user.email = user_update.email
    user.name = user_update.name
    await session.commit()
    await session.refresh(user)
    return user


async def delete_user(session, user_id):
    result = await session.execute(select(User).filter_by(id=user_id))
    user = result.scalar_one_or_none()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    await session.delete(user)
    await session.commit()
    return user
