from fastapi import APIRouter, WebSocket, Depends, WebSocketDisconnect, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.db import get_session
from app.websocket.connection_manager import ConnectionManager
from app.schemas import ChatMessageCreate, ChatMessage
from app.models import User
from app.crud import chat as crud_chat
from typing import List

from datetime import datetime

router = APIRouter()
manager = ConnectionManager()

# Websocket
@router.websocket("/{user_id}")
async def websocket_chat(
    websocket: WebSocket, user_id: int, session: AsyncSession = Depends(get_session)
):
    # verify user_id
    result = await session.execute(select(User).filter_by(id=user_id))
    user = result.scalar_one_or_none()
    if user is None:
        await websocket.close(code=1008, reason="Unauthorized")
        return
    username = user.name
    await manager.connect(user_id, websocket)

    # Broadcast user join
    await manager.broadcast(
        {
            "user_id": user_id,
            "username": username,
            "message": f"User {username} joined the chat",
            "timestamp": datetime.utcnow().isoformat(),
        }
    )

    try:
        while True:
            message_data = await websocket.receive_json()
            recipient_id = message_data.get("recipient_id")
            
            # Save message to DB
            chat_message_create = ChatMessageCreate(
                user_id=user_id,
                message=message_data["message"],
                recipient_id=recipient_id,
            )
            chat_message = await crud_chat.create_chat_message(
                session, chat_message_create
            )
            
            # Send message to clients
            message = {
                    "user_id": chat_message.user_id,
                    "username": username,
                    "message": chat_message.message,
                    "timestamp": chat_message.timestamp.isoformat(),
                    "recipient_id": recipient_id,
                }

            if recipient_id:
                recipient_id = int(recipient_id)
                # Handle private message
                ## send to the sender's connection
                await manager.send_personal_message(message, websocket)
                ## send to the recipient's connection                
                recipient_connections = manager.active_connections.get(recipient_id, [])
                for connection in recipient_connections:
                    await manager.send_personal_message(message, connection)
            else:
                # Handle public message
                await manager.broadcast(message)

    except WebSocketDisconnect:
        manager.disconnect(user_id, websocket)
        await manager.broadcast(
            {
                "user_id": user_id,
                "username": username,
                "message": f"User {username} left the chat",
                "timestamp": datetime.utcnow().isoformat(),
            }
        )
        
# CRUD
@router.get("/messages", response_model=List[ChatMessage])
async def get_all_messages(session: AsyncSession = Depends(get_session), limit: int = 100):
    messages = await crud_chat.get_chat_messages(session, limit=limit)
    return messages


@router.get("/messages/{user_id}", response_model=List[ChatMessage])
async def get_messages(user_id: int, session: AsyncSession = Depends(get_session), limit: int = 100):
    # verify user_id
    result = await session.execute(select(User).filter_by(id=user_id))
    user = result.scalar_one_or_none()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    messages = await crud_chat.get_chat_messages_by_user(session, user_id, limit=limit)
    return messages