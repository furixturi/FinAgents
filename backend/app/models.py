from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, func, Enum, Text, JSON, TIMESTAMP

from enum import Enum as PyEnum

Base = declarative_base()

# Agent Group Chat related

class AgentType(PyEnum):
    ConversableAgent = "ConversableAgent"
    UserProxyAgent = "UserProxyAgent"
    AssistantAgent = "AssistantAgent"
    
class AIAgent(Base):
    __tablename__ = 'ai_agents'
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    agent_type = Column(Enum(AgentType), nullable=False)
    system_message = Column(String, default="You are a helpful AI Assistant.")
    is_termination_msg = Column(Text, nullable=False)
    max_consecutive_autoreply = Column(Integer, nullable=True)
    human_input_mode = Column(Enum('ALWAYS', 'NEVER', 'TERMINATE'), default='TERMINATE')
    function_map = Column(JSON, nullable=True)
    code_execution_config = Column(JSON, nullable=True)
    llm_config = Column(JSON, nullable=True)
    default_auto_reply = Column(Text, default='')
    description = Column(Text, nullable=True)
    chat_messages = Column(JSON, nullable=True)
    created_at = Column(TIMESTAMP, server_default=func.current_timestamp())

class AgentGroup(Base):
    __tablename__ = 'agent_groups'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    created_by = Column(Integer, ForeignKey('users.id'), nullable=False)
    manager_id = Column(Integer, ForeignKey('ai_agents.id'), nullable=False)
    creator_user_proxy_id = Column(Integer, ForeignKey('ai_agents.id'), nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.current_timestamp())

class AgentGroupMember(Base):
    __tablename__ = 'agent_group_members'
    group_id = Column(Integer, ForeignKey('groups.id'), primary_key=True, nullable=False)
    agent_id = Column(Integer, ForeignKey('agents.id'), primary_key=True, nullable=False)
    added_at = Column(TIMESTAMP, server_default=func.current_timestamp())

class AgentGroupMessage(Base):
    __tablename__ = 'agent_group_messages'
    id = Column(Integer, primary_key=True, autoincrement=True)
    group_id = Column(Integer, ForeignKey('agent_groups.id'), nullable=False)
    sender_id = Column(Integer, ForeignKey('agents.id'), nullable=False)
    message = Column(Text, nullable=False)
    sent_at = Column(TIMESTAMP, server_default=func.current_timestamp())

# User 
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)

# Post
class Post(Base):
    __tablename__ = 'posts'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    content = Column(String)
    file_url = Column(String, nullable=True)
    user_id = Column(Integer, ForeignKey('users.id'))

    author = relationship("User")

# Chat
class ChatMessage(Base):
    __tablename__ = 'chat_messages'
    id = Column(Integer, primary_key=True, index=True)
    message = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    recipient_id = Column(Integer, ForeignKey('users.id'), nullable=True)
    timestamp = Column(DateTime, server_default=func.now())
    
    user = relationship("User", foreign_keys=[user_id])
    recipient = relationship("User", foreign_keys=[recipient_id])

# Session    
class SessionModel(Base):
    __tablename__ = 'sessions'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    session_data = Column(String)  # JSON or any other serialized format

    user = relationship("User")
