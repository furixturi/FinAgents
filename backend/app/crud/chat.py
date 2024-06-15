from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.schemas import ChatMessageCreate
from app.models import ChatMessage


async def create_chat_message(
    session: AsyncSession, chat_message_create: ChatMessageCreate
):
    chat_message = ChatMessage(
        user_id=chat_message_create.user_id,
        recipient_id=chat_message_create.recipient_id,
        message=chat_message_create.message,
    )
    session.add(chat_message)
    await session.commit()
    await session.refresh(chat_message)
    return chat_message


async def get_chat_messages_by_user(session: AsyncSession, user_id: int, limit: int = 100):
    result = await session.execute(
        select(ChatMessage)
        .filter_by(user_id=user_id)
        .order_by(ChatMessage.timestamp.desc())
        .limit(limit)
    )
    messages = result.scalars().all()
    return messages

async def get_chat_messages(session: AsyncSession, limit: int = 100):
    result = await session.execute(
        select(ChatMessage)
        .order_by(ChatMessage.timestamp.desc())
        .limit(limit)
    )
    messages = result.scalars().all()
    return messages