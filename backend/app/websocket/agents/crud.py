from sqlalchemy.orm import Session
from . import models, schemas


# CRUD operations for AI_Agent
async def create_ai_agent(db: Session, ai_agent: schemas.AIAgentCreate):
    db_ai_agent = models.AIAgent(**ai_agent.dict())
    db.add(db_ai_agent)
    db.commit()
    db.refresh(db_ai_agent)
    return db_ai_agent


async def get_ai_agent(db: Session, agent_id: int):
    return db.query(models.AIAgent).filter(models.AIAgent.id == agent_id).first()


async def get_ai_agents(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.AIAgent).offset(skip).limit(limit).all()


async def update_ai_agent(db: Session, agent_id: int, ai_agent: schemas.AIAgentCreate):
    db_ai_agent = db.query(models.AIAgent).filter(models.AIAgent.id == agent_id).first()
    if db_ai_agent:
        for key, value in ai_agent.dict().items():
            setattr(db_ai_agent, key, value)
        db.commit()
        db.refresh(db_ai_agent)
        return db_ai_agent
    return None


async def delete_ai_agent(db: Session, agent_id: int):
    db_ai_agent = db.query(models.AIAgent).filter(models.AIAgent.id == agent_id).first()
    if db_ai_agent:
        db.delete(db_ai_agent)
        db.commit()
        return db_ai_agent
    return None


# CRUD operations for AgentGroup
async def create_agent_group(db: Session, agent_group: schemas.AgentGroupCreate):
    db_agent_group = models.AgentGroup(**agent_group.dict())
    db.add(db_agent_group)
    db.commit()
    db.refresh(db_agent_group)
    return db_agent_group


async def get_agent_group(db: Session, group_id: int):
    return db.query(models.AgentGroup).filter(models.AgentGroup.id == group_id).first()


async def get_agent_groups(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.AgentGroup).offset(skip).limit(limit).all()


async def update_agent_group(
    db: Session, group_id: int, agent_group: schemas.AgentGroupCreate
):
    db_agent_group = (
        db.query(models.AgentGroup).filter(models.AgentGroup.id == group_id).first()
    )
    if db_agent_group:
        for key, value in agent_group.dict().items():
            setattr(db_agent_group, key, value)
        db.commit()
        db.refresh(db_agent_group)
        return db_agent_group
    return None


async def delete_agent_group(db: Session, group_id: int):
    db_agent_group = (
        db.query(models.AgentGroup).filter(models.AgentGroup.id == group_id).first()
    )
    if db_agent_group:
        db.delete(db_agent_group)
        db.commit()
        return db_agent_group
    return None


# CRUD operations for AgentGroupMember
async def create_agent_group_member(
    db: Session, agent_group_member: schemas.AgentGroupMemberCreate
):
    db_agent_group_member = models.AgentGroupMember(**agent_group_member.dict())
    db.add(db_agent_group_member)
    db.commit()
    db.refresh(db_agent_group_member)
    return db_agent_group_member


async def get_agent_group_member(db: Session, group_id: int, agent_id: int):
    return (
        db.query(models.AgentGroupMember)
        .filter(
            models.AgentGroupMember.group_id == group_id,
            models.AgentGroupMember.agent_id == agent_id,
        )
        .first()
    )


async def get_agent_group_members(
    db: Session, group_id: int, skip: int = 0, limit: int = 100
):
    return (
        db.query(models.AgentGroupMember)
        .filter(models.AgentGroupMember.group_id == group_id)
        .offset(skip)
        .limit(limit)
        .all()
    )


async def delete_agent_group_member(db: Session, group_id: int, agent_id: int):
    db_agent_group_member = (
        db.query(models.AgentGroupMember)
        .filter(
            models.AgentGroupMember.group_id == group_id,
            models.AgentGroupMember.agent_id == agent_id,
        )
        .first()
    )
    if db_agent_group_member:
        db.delete(db_agent_group_member)
        db.commit()
        return db_agent_group_member
    return None


# CRUD operations for AgentGroupMessage
async def create_agent_group_message(
    db: Session, agent_group_message: schemas.AgentGroupMessageCreate
):
    db_agent_group_message = models.AgentGroupMessage(**agent_group_message.dict())
    db.add(db_agent_group_message)
    db.commit()
    db.refresh(db_agent_group_message)
    return db_agent_group_message


async def get_agent_group_message(db: Session, message_id: int):
    return (
        db.query(models.AgentGroupMessage)
        .filter(models.AgentGroupMessage.id == message_id)
        .first()
    )


async def get_agent_group_messages(
    db: Session, group_id: int, skip: int = 0, limit: int = 100
):
    return (
        db.query(models.AgentGroupMessage)
        .filter(models.AgentGroupMessage.group_id == group_id)
        .offset(skip)
        .limit(limit)
        .all()
    )


async def delete_agent_group_message(db: Session, message_id: int):
    db_agent_group_message = (
        db.query(models.AgentGroupMessage)
        .filter(models.AgentGroupMessage.id == message_id)
        .first()
    )
    if db_agent_group_message:
        db.delete(db_agent_group_message)
        db.commit()
        return db_agent_group_message
    return None
