from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.db import get_session
from app.schemas import AgentGroupMessage, AgentGroupMessageCreate
from app.crud import agent_group_message as crud_agent_group_message
from typing import List

router = APIRouter()

# prefix /ai_agents/users/{user_id}/agent_groups/{group_id}/messages


@router.post("/", response_model=AgentGroupMessage)
async def create_agent_group_message(
    user_id: int,
    group_id: int,
    agent_group_message_create: AgentGroupMessageCreate,
    session: AsyncSession = Depends(get_session)
):
    agent_group_message_create.group_id = group_id
    agent_group_message_create.sender_id = user_id
    return await crud_agent_group_message.user_create_agent_group_message(session, user_id, agent_group_message_create)

@router.get("/", response_model=List[AgentGroupMessage])
async def get_agent_group_messages(
    user_id: int,
    group_id: int,
    skip: int = 0,
    limit: int = 100,
    session: AsyncSession = Depends(get_session)
):
    return await crud_agent_group_message.user_get_agent_group_messages(session, user_id, group_id, skip, limit)

@router.get("/{message_id}", response_model=AgentGroupMessage)
async def get_agent_group_message(
    user_id: int,
    group_id: int,
    message_id: int,
    session: AsyncSession = Depends(get_session)
):
    agent_group_message = await crud_agent_group_message.user_get_agent_group_message(session, user_id, group_id, message_id)
    if not agent_group_message:
        raise HTTPException(status_code=404, detail="Agent Group Message not found")
    return agent_group_message

@router.delete("/{message_id}", response_model=AgentGroupMessage)
async def delete_agent_group_message(
    user_id: int,
    group_id: int,
    message_id: int,
    session: AsyncSession = Depends(get_session)
):
    agent_group_message = await crud_agent_group_message.user_delete_agent_group_message(session, user_id, group_id, message_id)
    if not agent_group_message:
        raise HTTPException(status_code=404, detail="Agent Group Message not found")
    return agent_group_message
