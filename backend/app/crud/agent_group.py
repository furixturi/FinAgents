from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List
from app.models import AgentGroup
from app.schemas import AgentGroupCreate, AgentGroupUpdate

# Admin CRUD functions
async def admin_create_agent_group(db: AsyncSession, agent_group_create: AgentGroupCreate) -> AgentGroup:
    agent_group = AgentGroup(**agent_group_create.dict())
    db.add(agent_group)
    await db.commit()
    await db.refresh(agent_group)
    return agent_group

async def admin_get_agent_groups(db: AsyncSession, skip: int = 0, limit: int = 100) -> List[AgentGroup]:
    result = await db.execute(select(AgentGroup).offset(skip).limit(limit))
    return result.scalars().all()

async def admin_get_agent_group(db: AsyncSession, group_id: int) -> AgentGroup:
    result = await db.execute(select(AgentGroup).where(AgentGroup.id == group_id))
    return result.scalars().first()

async def admin_update_agent_group(db: AsyncSession, group_id: int, agent_group_update: AgentGroupUpdate) -> AgentGroup:
    result = await db.execute(select(AgentGroup).where(AgentGroup.id == group_id))
    agent_group = result.scalars().first()
    if agent_group:
        for key, value in agent_group_update.dict(exclude_unset=True).items():
            setattr(agent_group, key, value)
        await db.commit()
        await db.refresh(agent_group)
    return agent_group

async def admin_delete_agent_group(db: AsyncSession, group_id: int) -> AgentGroup:
    result = await db.execute(select(AgentGroup).where(AgentGroup.id == group_id))
    agent_group = result.scalars().first()
    if agent_group:
        await db.delete(agent_group)
        await db.commit()
    return agent_group

# User CRUD functions
async def user_create_agent_group(db: AsyncSession, agent_group_create: AgentGroupCreate) -> AgentGroup:
    agent_group = AgentGroup(**agent_group_create.dict())
    db.add(agent_group)
    await db.commit()
    await db.refresh(agent_group)
    return agent_group

async def user_get_agent_groups(db: AsyncSession, user_id: int, skip: int = 0, limit: int = 100) -> List[AgentGroup]:
    result = await db.execute(select(AgentGroup).where(AgentGroup.created_by == user_id).offset(skip).limit(limit))
    return result.scalars().all()

async def user_get_agent_group(db: AsyncSession, user_id: int, group_id: int) -> AgentGroup:
    result = await db.execute(select(AgentGroup).where(AgentGroup.id == group_id, AgentGroup.created_by == user_id))
    return result.scalars().first()

async def user_update_agent_group(db: AsyncSession, user_id: int, group_id: int, agent_group_update: AgentGroupUpdate) -> AgentGroup:
    result = await db.execute(select(AgentGroup).where(AgentGroup.id == group_id, AgentGroup.created_by == user_id))
    agent_group = result.scalars().first()
    if agent_group:
        for key, value in agent_group_update.dict(exclude_unset=True).items():
            setattr(agent_group, key, value)
        await db.commit()
        await db.refresh(agent_group)
    return agent_group

async def user_delete_agent_group(db: AsyncSession, user_id: int, group_id: int) -> AgentGroup:
    result = await db.execute(select(AgentGroup).where(AgentGroup.id == group_id, AgentGroup.created_by == user_id))
    agent_group = result.scalars().first()
    if agent_group:
        await db.delete(agent_group)
        await db.commit()
    return agent_group
