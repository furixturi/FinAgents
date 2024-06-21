from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.db import get_session
from app.schemas import AgentGroupMessage, AgentGroupMessageCreate, AgentGroupMessageUpdate
from app.crud import agent_group_message as crud_agent_group_message, agent_group as crud_agent_group
from typing import List

router = APIRouter()

# prefix /agents/users/{user_id}/agent_groups/{group_id}/messages


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

@router.put("/{message_id}", response_model=AgentGroupMessage)
async def update_agent_group_message(
    user_id: int,
    group_id: int,
    message_id: int,
    agent_group_message_update: AgentGroupMessageUpdate,
    session: AsyncSession = Depends(get_session)
):
    # Ensure that the user created the group since agent group message only has info of the agent's id (sender_id), not user_id
    agent_group = await crud_agent_group.user_get_agent_group(session, user_id, group_id)
    if not agent_group:
        raise HTTPException(status_code=403, detail="Not authorized to update messages of this group")
    
    return await crud_agent_group_message.user_update_agent_group_message(session, group_id, message_id, agent_group_message_update)

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
