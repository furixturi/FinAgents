from fastapi import APIRouter, Depends, HTTPException, WebSocket
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.db import get_session
from app.models import User, AgentGroup
from app.agents.agent_group_connection_manager import AgentGroupConnectionManager

from app.agents.agent_group_chat import AgentGroupChat
from typing import List

router = APIRouter()
# prefix: /agents/users/{user_id}/groupchat
ws_connection_manager = AgentGroupConnectionManager()

@router.post("/create-dummy-group")
async def create_dummy_group(
    user_id: int,
    db: AsyncSession = Depends(get_session)
):
    # verify user_id and retrieve the user
    result = await db.execute(select(User).filter_by(id=user_id))
    user = result.scalar_one_or_none()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    try:
        dummy_group_chat: AgentGroupChat = await AgentGroupChat.create(db=db, user_id=user_id, dummy=True)
        group_id = dummy_group_chat.group_id
        return {"group_id": group_id}
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=str(e))


@router.websocket("/{group_id}")
async def init_agent_group(
    websocket: WebSocket,
    user_id: int,
    group_id: int,
    db: AsyncSession = Depends(get_session),
):
    # verify user_id and retrieve the user
    result = await db.execute(select(User).filter_by(id=user_id))
    user = result.scalar_one_or_none()
    if user is None:
        await websocket.close(code=1008, reason="Unauthorized")
        return
    
    # verify group_id and retrieve the group
    result = await db.execute(select(AgentGroup).where(AgentGroup.id == group_id, AgentGroup.created_by == user_id))
    group = result.scalar_one_or_none()
    if group is None:
        await websocket.close(code=1008, reason="Group not found")
        return    
    
    # create an agent group chat instance and kick off the chat
    await ws_connection_manager.connect(user_id, group_id, websocket)
    
    agent_group_chat = AgentGroupChat(db=db, user_id=user_id, group_id=group_id)
    
    # receive the first user message to kick off the chat
    first_message = await websocket.receive_text()
    agent_group_chat.start_chat(first_message)
    
    
    
