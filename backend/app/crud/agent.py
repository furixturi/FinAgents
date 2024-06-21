from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List
from app.models import AIAgent
from app.schemas import AIAgentCreate, AIAgentUpdate

# Admin CRUD functions
async def admin_create_ai_agent(db: AsyncSession, ai_agent_create: AIAgentCreate) -> AIAgent:
    ai_agent = AIAgent(**ai_agent_create.dict())
    db.add(ai_agent)
    await db.commit()
    await db.refresh(ai_agent)
    return ai_agent

async def admin_get_ai_agents(db: AsyncSession, skip: int = 0, limit: int = 100) -> List[AIAgent]:
    result = await db.execute(select(AIAgent).offset(skip).limit(limit))
    return result.scalars().all()

async def admin_get_ai_agent(db: AsyncSession, agent_id: int) -> AIAgent:
    result = await db.execute(select(AIAgent).where(AIAgent.id == agent_id))
    return result.scalars().first()

async def admin_update_ai_agent(db: AsyncSession, agent_id: int, ai_agent_update: AIAgentUpdate) -> AIAgent:
    result = await db.execute(select(AIAgent).where(AIAgent.id == agent_id))
    ai_agent = result.scalars().first()
    if ai_agent:
        for key, value in ai_agent_update.dict(exclude_unset=True).items():
            setattr(ai_agent, key, value)
        await db.commit()
        await db.refresh(ai_agent)
    return ai_agent

async def admin_delete_ai_agent(db: AsyncSession, agent_id: int) -> AIAgent:
    result = await db.execute(select(AIAgent).where(AIAgent.id == agent_id))
    ai_agent = result.scalars().first()
    if ai_agent:
        await db.delete(ai_agent)
        await db.commit()
    return ai_agent

# User CRUD functions
async def user_create_ai_agent(db: AsyncSession, ai_agent_create: AIAgentCreate) -> AIAgent:
    ai_agent = AIAgent(**ai_agent_create.dict())
    db.add(ai_agent)
    await db.commit()
    await db.refresh(ai_agent)
    return ai_agent

async def user_get_ai_agents(db: AsyncSession, user_id: int, skip: int = 0, limit: int = 100) -> List[AIAgent]:
    result = await db.execute(select(AIAgent).where(AIAgent.user_id == user_id).offset(skip).limit(limit))
    return result.scalars().all()

async def user_get_ai_agent(db: AsyncSession, user_id: int, agent_id: int) -> AIAgent:
    result = await db.execute(select(AIAgent).where(AIAgent.id == agent_id, AIAgent.user_id == user_id))
    return result.scalars().first()

async def user_update_ai_agent(db: AsyncSession, user_id: int, agent_id: int, ai_agent_update: AIAgentUpdate) -> AIAgent:
    result = await db.execute(select(AIAgent).where(AIAgent.id == agent_id, AIAgent.user_id == user_id))
    ai_agent = result.scalars().first()
    if ai_agent:
        for key, value in ai_agent_update.dict(exclude_unset=True).items():
            setattr(ai_agent, key, value)
        await db.commit()
        await db.refresh(ai_agent)
    return ai_agent

async def user_delete_ai_agent(db: AsyncSession, user_id: int, agent_id: int) -> AIAgent:
    result = await db.execute(select(AIAgent).where(AIAgent.id == agent_id, AIAgent.user_id == user_id))
    ai_agent = result.scalars().first()
    if ai_agent:
        await db.delete(ai_agent)
        await db.commit()
    return ai_agent