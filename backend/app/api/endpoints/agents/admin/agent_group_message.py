from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.db import get_session
from app.schemas import AgentGroupMessage, AgentGroupMessageCreate
from app.crud import agent_group_message as crud_agent_group_message
from typing import List

router = APIRouter()

# prefix /ai_agents/admin/agent_groups/{group_id}/messages

@router.post("/", response_model=AgentGroupMessage)
async def create_agent_group_message(
    agent_group_message_create: AgentGroupMessageCreate,
    session: AsyncSession = Depends(get_session)
):
    return await crud_agent_group_message.admin_create_agent_group_message(session, agent_group_message_create)

@router.get("/", response_model=List[AgentGroupMessage])
async def get_agent_group_messages(
    group_id: int,
    skip: int = 0,
    limit: int = 100,
    session: AsyncSession = Depends(get_session)
):
    return await crud_agent_group_message.admin_get_agent_group_messages(session, group_id, skip, limit)

@router.get("/{message_id}", response_model=AgentGroupMessage)
async def get_agent_group_message(
    message_id: int,
    session: AsyncSession = Depends(get_session)
):
    agent_group_message = await crud_agent_group_message.admin_get_agent_group_message(session, message_id)
    if not agent_group_message:
        raise HTTPException(status_code=404, detail="Agent Group Message not found")
    return agent_group_message

@router.delete("/{message_id}", response_model=AgentGroupMessage)
async def delete_agent_group_message(
    message_id: int,
    session: AsyncSession = Depends(get_session)
):
    agent_group_message = await crud_agent_group_message.admin_delete_agent_group_message(session, message_id)
    if not agent_group_message:
        raise HTTPException(status_code=404, detail="Agent Group Message not found")
    return agent_group_message