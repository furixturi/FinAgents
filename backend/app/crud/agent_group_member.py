from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List
from app.models import AgentGroupMember
from app.schemas import AgentGroupMemberCreate

# Admin CRUD functions
async def admin_create_agent_group_member(db: AsyncSession, agent_group_member_create: AgentGroupMemberCreate) -> AgentGroupMember:
    agent_group_member = AgentGroupMember(**agent_group_member_create.dict())
    db.add(agent_group_member)
    await db.commit()
    await db.refresh(agent_group_member)
    return agent_group_member

async def admin_get_agent_group_members(db: AsyncSession, group_id: int, skip: int = 0, limit: int = 100) -> List[AgentGroupMember]:
    result = await db.execute(select(AgentGroupMember).where(AgentGroupMember.group_id == group_id).offset(skip).limit(limit))
    return result.scalars().all()

async def admin_get_agent_group_member(db: AsyncSession, group_id: int, agent_id: int) -> AgentGroupMember:
    result = await db.execute(select(AgentGroupMember).where(AgentGroupMember.group_id == group_id, AgentGroupMember.agent_id == agent_id))
    return result.scalars().first()

async def admin_delete_agent_group_member(db: AsyncSession, group_id: int, agent_id: int) -> AgentGroupMember:
    result = await db.execute(select(AgentGroupMember).where(AgentGroupMember.group_id == group_id, AgentGroupMember.agent_id == agent_id))
    agent_group_member = result.scalars().first()
    if agent_group_member:
        await db.delete(agent_group_member)
        await db.commit()
    return agent_group_member

# User CRUD functions with validation
async def user_create_agent_group_member(db: AsyncSession, agent_group_member_create: AgentGroupMemberCreate) -> AgentGroupMember:
    agent_group_member = AgentGroupMember(**agent_group_member_create.dict())
    db.add(agent_group_member)
    await db.commit()
    await db.refresh(agent_group_member)
    return agent_group_member

async def user_get_agent_group_members(db: AsyncSession, group_id: int, skip: int = 0, limit: int = 100) -> List[AgentGroupMember]:
    result = await db.execute(select(AgentGroupMember).where(AgentGroupMember.group_id == group_id).offset(skip).limit(limit))
    return result.scalars().all()

async def user_get_agent_group_member(db: AsyncSession, group_id: int, agent_id: int) -> AgentGroupMember:
    result = await db.execute(select(AgentGroupMember).where(AgentGroupMember.group_id == group_id, AgentGroupMember.agent_id == agent_id))
    return result.scalars().first()

async def user_delete_agent_group_member(db: AsyncSession, group_id: int, agent_id: int) -> AgentGroupMember:
    result = await db.execute(select(AgentGroupMember).where(AgentGroupMember.group_id == group_id, AgentGroupMember.agent_id == agent_id))
    agent_group_member = result.scalars().first()
    if agent_group_member:
        await db.delete(agent_group_member)
        await db.commit()
    return agent_group_member
