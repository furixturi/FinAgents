from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List
from app.models import AIAgent
from app.schemas import AIAgentCreate, AIAgentUpdate

# Admin CRUD functions
async def admin_create_agent(db: AsyncSession, agent_create: AIAgentCreate) -> AIAgent:
    agent = AIAgent(**agent_create.dict())
    db.add(agent)
    await db.commit()
    await db.refresh(agent)
    return agent

async def admin_get_agents(db: AsyncSession, skip: int = 0, limit: int = 100) -> List[AIAgent]:
    result = await db.execute(select(AIAgent).offset(skip).limit(limit))
    return result.scalars().all()

async def admin_get_agent(db: AsyncSession, agent_id: int) -> AIAgent:
    result = await db.execute(select(AIAgent).where(AIAgent.id == agent_id))
    return result.scalars().first()

async def admin_update_agent(db: AsyncSession, agent_id: int, agent_update: AIAgentUpdate) -> AIAgent:
    result = await db.execute(select(AIAgent).where(AIAgent.id == agent_id))
    agent = result.scalars().first()
    if agent:
        for key, value in agent_update.dict(exclude_unset=True).items():
            setattr(agent, key, value)
        await db.commit()
        await db.refresh(agent)
    return agent

async def admin_delete_agent(db: AsyncSession, agent_id: int) -> AIAgent:
    result = await db.execute(select(AIAgent).where(AIAgent.id == agent_id))
    agent = result.scalars().first()
    if agent:
        await db.delete(agent)
        await db.commit()
    return agent

# User CRUD functions
async def user_create_agent(db: AsyncSession, agent_create: AIAgentCreate) -> AIAgent:
    agent = AIAgent(**agent_create.dict())
    db.add(agent)
    await db.commit()
    await db.refresh(agent)
    return agent

async def user_get_agents(db: AsyncSession, user_id: int, skip: int = 0, limit: int = 100) -> List[AIAgent]:
    result = await db.execute(select(AIAgent).where(AIAgent.user_id == user_id).offset(skip).limit(limit))
    return result.scalars().all()

async def user_get_agent(db: AsyncSession, user_id: int, agent_id: int) -> AIAgent:
    result = await db.execute(select(AIAgent).where(AIAgent.id == agent_id, AIAgent.user_id == user_id))
    return result.scalars().first()

async def user_update_agent(db: AsyncSession, user_id: int, agent_id: int, agent_update: AIAgentUpdate) -> AIAgent:
    result = await db.execute(select(AIAgent).where(AIAgent.id == agent_id, AIAgent.user_id == user_id))
    agent = result.scalars().first()
    if agent:
        for key, value in agent_update.dict(exclude_unset=True).items():
            setattr(agent, key, value)
        await db.commit()
        await db.refresh(agent)
    return agent

async def user_delete_agent(db: AsyncSession, user_id: int, agent_id: int) -> AIAgent:
    result = await db.execute(select(AIAgent).where(AIAgent.id == agent_id, AIAgent.user_id == user_id))
    agent = result.scalars().first()
    if agent:
        await db.delete(agent)
        await db.commit()
    return agent