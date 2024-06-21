from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.db import get_session
from app.schemas import AgentGroupMember, AgentGroupMemberCreate
from app.crud import agent_group_member as crud_agent_group_member
from typing import List

router = APIRouter()

# prefix: /agents/users/{user_id}/agent_groups/{group_id}/members

@router.post("/", response_model=AgentGroupMember)
async def create_agent_group_member(
    user_id: int,
    group_id: int,
    agent_group_member_create: AgentGroupMemberCreate,
    session: AsyncSession = Depends(get_session)
):
    agent_group_member_create.group_id = group_id
    return await crud_agent_group_member.user_create_agent_group_member(session, user_id, agent_group_member_create)

@router.get("/", response_model=List[AgentGroupMember])
async def get_agent_group_members(
    user_id: int,
    group_id: int,
    skip: int = 0,
    limit: int = 100,
    session: AsyncSession = Depends(get_session)
):
    return await crud_agent_group_member.user_get_agent_group_members(session, user_id, group_id, skip, limit)

@router.get("/{agent_id}", response_model=AgentGroupMember)
async def get_agent_group_member(
    user_id: int,
    group_id: int,
    agent_id: int,
    session: AsyncSession = Depends(get_session)
):
    agent_group_member = await crud_agent_group_member.user_get_agent_group_member(session, user_id, group_id, agent_id)
    if not agent_group_member:
        raise HTTPException(status_code=404, detail="Agent Group Member not found")
    return agent_group_member

@router.delete("/{agent_id}", response_model=AgentGroupMember)
async def delete_agent_group_member(
    user_id: int,
    group_id: int,
    agent_id: int,
    session: AsyncSession = Depends(get_session)
):
    agent_group_member = await crud_agent_group_member.user_delete_agent_group_member(session, user_id, group_id, agent_id)
    if not agent_group_member:
        raise HTTPException(status_code=404, detail="Agent Group Member not found")
    return agent_group_member