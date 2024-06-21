from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.db import get_session
from app.schemas import AIAgent, AIAgentCreate, AIAgentUpdate
from app.crud import agent as crud_agent
from typing import List

router = APIRouter()
# prefix: /agents/users/{user_id}/agents


@router.post("/", response_model=AIAgent)
async def create_agent(
    user_id: int,
    agent_create: AIAgentCreate,
    session: AsyncSession = Depends(get_session)
):
    agent_create.user_id = user_id
    return await crud_agent.user_create_agent(session, agent_create)

@router.get("/", response_model=List[AIAgent])
async def get_agents(
    user_id: int,
    skip: int = 0,
    limit: int = 100,
    session: AsyncSession = Depends(get_session)
):
    return await crud_agent.user_get_agents(session, user_id, skip, limit)

@router.get("/{agent_id}", response_model=AIAgent)
async def get_agent(
    user_id: int,
    agent_id: int,
    session: AsyncSession = Depends(get_session)
):
    agent = await crud_agent.user_get_agent(session, user_id, agent_id)
    if not agent:
        raise HTTPException(status_code=404, detail="AI Agent not found")
    return agent

@router.put("/{agent_id}", response_model=AIAgent)
async def update_agent(
    user_id: int,
    agent_id: int,
    agent_update: AIAgentUpdate,
    session: AsyncSession = Depends(get_session)
):
    agent = await crud_agent.user_update_agent(session, user_id, agent_id, agent_update)
    if not agent:
        raise HTTPException(status_code=404, detail="AI Agent not found")
    return agent

@router.delete("/{agent_id}", response_model=AIAgent)
async def delete_agent(
    user_id: int,
    agent_id: int,
    session: AsyncSession = Depends(get_session)
):
    agent = await crud_agent.user_delete_agent(session, user_id, agent_id)
    if not agent:
        raise HTTPException(status_code=404, detail="AI Agent not found")
    return agent