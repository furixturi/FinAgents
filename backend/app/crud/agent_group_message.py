from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List
from app.models import AgentGroupMessage
from app.schemas import AgentGroupMessageCreate, AgentGroupMessageUpdate

# Admin CRUD functions
async def admin_create_agent_group_message(db: AsyncSession, agent_group_message_create: AgentGroupMessageCreate) -> AgentGroupMessage:
    agent_group_message = AgentGroupMessage(**agent_group_message_create.dict())
    db.add(agent_group_message)
    await db.commit()
    await db.refresh(agent_group_message)
    return agent_group_message

async def admin_get_agent_group_messages(db: AsyncSession, group_id: int, skip: int = 0, limit: int = 100) -> List[AgentGroupMessage]:
    result = await db.execute(select(AgentGroupMessage).where(AgentGroupMessage.group_id == group_id).offset(skip).limit(limit))
    return result.scalars().all()

async def admin_get_agent_group_message(db: AsyncSession, message_id: int) -> AgentGroupMessage:
    result = await db.execute(select(AgentGroupMessage).where(AgentGroupMessage.id == message_id))
    return result.scalars().first()

async def admin_delete_agent_group_message(db: AsyncSession, message_id: int) -> AgentGroupMessage:
    result = await db.execute(select(AgentGroupMessage).where(AgentGroupMessage.id == message_id))
    agent_group_message = result.scalars().first()
    if agent_group_message:
        await db.delete(agent_group_message)
        await db.commit()
    return agent_group_message

async def admin_update_agent_group_message(db: AsyncSession, message_id: int, agent_group_message_update: AgentGroupMessageUpdate) -> AgentGroupMessage:
    result = await db.execute(select(AgentGroupMessage).where(AgentGroupMessage.id == message_id))
    agent_group_message = result.scalars().first()
    if agent_group_message:
        for key, value in agent_group_message_update.dict(exclude_unset=True).items():
            setattr(agent_group_message, key, value)
        await db.commit()
        await db.refresh(agent_group_message)
    return agent_group_message

# User CRUD functions with validation
async def user_create_agent_group_message(db: AsyncSession, agent_group_message_create: AgentGroupMessageCreate) -> AgentGroupMessage:
    agent_group_message = AgentGroupMessage(**agent_group_message_create.dict())
    db.add(agent_group_message)
    await db.commit()
    await db.refresh(agent_group_message)
    return agent_group_message

async def user_get_agent_group_messages(db: AsyncSession, group_id: int, skip: int = 0, limit: int = 100) -> List[AgentGroupMessage]:
    result = await db.execute(select(AgentGroupMessage).where(AgentGroupMessage.group_id == group_id).offset(skip).limit(limit))
    return result.scalars().all()

async def user_get_agent_group_message(db: AsyncSession, group_id: int, message_id: int) -> AgentGroupMessage:
    result = await db.execute(select(AgentGroupMessage).where(AgentGroupMessage.id == message_id, AgentGroupMessage.group_id == group_id))
    return result.scalars().first()

async def user_delete_agent_group_message(db: AsyncSession, group_id: int, message_id: int) -> AgentGroupMessage:
    result = await db.execute(select(AgentGroupMessage).where(AgentGroupMessage.id == message_id, AgentGroupMessage.group_id == group_id))
    agent_group_message = result.scalars().first()
    if agent_group_message:
        await db.delete(agent_group_message)
        await db.commit()
    return agent_group_message

async def user_update_agent_group_message(db: AsyncSession, user_id: int, group_id: int, message_id: int, agent_group_message_update: AgentGroupMessageUpdate) -> AgentGroupMessage:
    result = await db.execute(select(AgentGroupMessage).where(AgentGroupMessage.id == message_id, AgentGroupMessage.group_id == group_id))
    agent_group_message = result.scalars().first()
    if agent_group_message:
        for key, value in agent_group_message_update.dict(exclude_unset=True).items():
            setattr(agent_group_message, key, value)
        await db.commit()
        await db.refresh(agent_group_message)
    return agent_group_message