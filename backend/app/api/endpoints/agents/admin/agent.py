from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.db import get_session
from app.schemas import AIAgent, AIAgentCreate, AIAgentUpdate
from app.crud import agent as crud_agent
from typing import List

router = APIRouter()

# prefix /ai_agents/admin/agents

@router.post("/", response_model=AIAgent)
async def create_ai_agent(
    ai_agent_create: AIAgentCreate,
    session: AsyncSession = Depends(get_session)
):
    return await crud_agent.admin_create_ai_agent(session, ai_agent_create)

@router.get("/", response_model=List[AIAgent])
async def get_ai_agents(
    skip: int = 0,
    limit: int = 100,
    session: AsyncSession = Depends(get_session)
):
    return await crud_agent.admin_get_ai_agents(session, skip, limit)

@router.get("/{agent_id}", response_model=AIAgent)
async def get_ai_agent(
    agent_id: int,
    session: AsyncSession = Depends(get_session)
):
    ai_agent = await crud_agent.admin_get_ai_agent(session, agent_id)
    if not ai_agent:
        raise HTTPException(status_code=404, detail="AI Agent not found")
    return ai_agent

@router.put("/{agent_id}", response_model=AIAgent)
async def update_ai_agent(
    agent_id: int,
    ai_agent_update: AIAgentUpdate,
    session: AsyncSession = Depends(get_session)
):
    ai_agent = await crud_agent.admin_update_ai_agent(session, agent_id, ai_agent_update)
    if not ai_agent:
        raise HTTPException(status_code=404, detail="AI Agent not found")
    return ai_agent

@router.delete("/{agent_id}", response_model=AIAgent)
async def delete_ai_agent(
    agent_id: int,
    session: AsyncSession = Depends(get_session)
):
    ai_agent = await crud_agent.admin_delete_ai_agent(session, agent_id)
    if not ai_agent:
        raise HTTPException(status_code=404, detail="AI Agent not found")
    return ai_agent