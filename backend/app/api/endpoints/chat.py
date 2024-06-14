from fastapi import APIRouter, WebSocket, Depends, WebSocketDisconnect, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.db import get_session
from app.connection_manager import ConnectionManager
from app.schemas import ChatMessageCreate, ChatMessage
from app.models import User
from app.crud import chat as crud_chat
from typing import List

from datetime import datetime

router = APIRouter()

manager = ConnectionManager()


@router.websocket("/{user_id}")
async def websocket_endpoint(
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
            chat_message_create = ChatMessageCreate(
                user_id=user_id,
                message=message_data["message"],
                recipient_id=recipient_id,
            )

            # Save message to DB
            chat_message = await crud_chat.create_chat_message(
                session, chat_message_create
            )
            
            message = {
                    "user_id": chat_message.user_id,
                    "username": username,
                    "message": chat_message.message,
                    "timestamp": chat_message.timestamp.isoformat(),
                    "recipient_id": recipient_id,
                }

            if recipient_id:
                # Handle private message
                if recipient_id in manager.active_connections:
                    for connection in manager.active_connections[recipient_id]:
                        await manager.send_personal_message(message, connection)
            else:
                # Handle public message
                await manager.broadcast(message)

    except WebSocketDisconnect:
        manager.disconnect(user_id, websocket)
        await manager.broadcast(
            {
                "user_id": chat_message.user_id,
                "username": username,
                "message": f"User {username} left the chat",
                "timestamp": datetime.utcnow().isoformat(),
            }
        )

@router.get("/{user_id}/messages", response_model=List[ChatMessage])
async def get_messages(user_id: int, session: AsyncSession = Depends(get_session), limit: int = 100):
    # verify user_id
    result = await session.execute(select(User).filter_by(id=user_id))
    user = result.scalar_one_or_none()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    messages = await crud_chat.get_chat_messages(session, user_id, limit=limit)
    return messages