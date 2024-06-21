from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.db import get_session
from app.schemas import AgentGroup, AgentGroupCreate, AgentGroupUpdate
from app.crud import agent_group as crud_agent_group
from typing import List

router = APIRouter()

# prefix: /ai_agents/users/{user_id}/agent_groups

@router.post("/", response_model=AgentGroup)
async def create_agent_group(
    user_id: int,
    agent_group_create: AgentGroupCreate,
    session: AsyncSession = Depends(get_session)
):
    agent_group_create.created_by = user_id
    return await crud_agent_group.user_create_agent_group(session, agent_group_create)

@router.get("/", response_model=List[AgentGroup])
async def get_agent_groups(
    user_id: int,
    skip: int = 0,
    limit: int = 100,
    session: AsyncSession = Depends(get_session)
):
    return await crud_agent_group.user_get_agent_groups(session, user_id, skip, limit)

@router.get("/{group_id}", response_model=AgentGroup)
async def get_agent_group(
    user_id: int,
    group_id: int,
    session: AsyncSession = Depends(get_session)
):
    agent_group = await crud_agent_group.user_get_agent_group(session, user_id, group_id)
    if not agent_group:
        raise HTTPException(status_code=404, detail="Agent Group not found")
    return agent_group

@router.put("/{group_id}", response_model=AgentGroup)
async def update_agent_group(
    user_id: int,
    group_id: int,
    agent_group_update: AgentGroupUpdate,
    session: AsyncSession = Depends(get_session)
):
    agent_group = await crud_agent_group.user_update_agent_group(session, user_id, group_id, agent_group_update)
    if not agent_group:
        raise HTTPException(status_code=404, detail="Agent Group not found")
    return agent_group

@router.delete("/{group_id}", response_model=AgentGroup)
async def delete_agent_group(
    user_id: int,
    group_id: int,
    session: AsyncSession = Depends(get_session)
):
    agent_group = await crud_agent_group.user_delete_agent_group(session, user_id, group_id)
    if not agent_group:
        raise HTTPException(status_code=404, detail="Agent Group not found")
    return agent_group