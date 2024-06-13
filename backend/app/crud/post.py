from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from app.models import Post, User
from app.schemas import PostCreate, PostUpdate


async def create_post(session: AsyncSession, post_create: PostCreate):
    # validate user_id
    result = await session.execute(select(User).filter_by(id=post_create.user_id))
    user = result.scalar_one_or_none()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    post = Post(
        title=post_create.title,
        content=post_create.content,
        user_id=post_create.user_id,
    )
    session.add(post)
    await session.commit()
    await session.refresh(post, attribute_names=['author'])
    await session.refresh(post.author, attribute_names=['posts'])
    return post


async def get_posts(session: AsyncSession):
    result = await session.execute(select(Post))
    posts = result.scalars().all()
    return posts


async def update_post(session: AsyncSession, post_id: int, post_update: PostUpdate):
    try:
        result = await session.execute(
            select(Post).filter_by(id=post_id)
        ).with_for_update()
        post = result.scalar_one_or_none()
        if post is None:
            raise HTTPException(status_code=404, defail="Post not found")
        post.title = post_update.title
        post.content = post_update.content
        await session.commit()
        await session.refresh(post)
    except TimeoutError:
        raise HTTPException(
            status_code=409,
            detail="Could not edit post due to concurrent update. Please try again.",
        )
    return post


async def delete_post(session: AsyncSession, post_id: int):
    result = await session.execute(select(Post).filter_by(id=post_id))
    post = result.scalar_one_or_none()
    if post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    await session.delete(post)
    await session.commit()
    return post
