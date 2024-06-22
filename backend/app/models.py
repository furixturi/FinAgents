from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    DateTime,
    func,
    Enum,
    Text,
    JSON,
    TIMESTAMP,
    Boolean,
)

from enum import Enum as PyEnum

Base = declarative_base()

# Agent Group Chat related


class AgentType(PyEnum):
    ConversableAgent = "ConversableAgent"
    UserProxyAgent = "UserProxyAgent"
    AssistantAgent = "AssistantAgent"


class AIAgent(Base):
    __tablename__ = "agents"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    agent_type = Column(Enum(AgentType), nullable=False)
    system_message = Column(String, default="You are a helpful AI Assistant.")
    is_termination_msg = Column(Text, nullable=False)
    max_consecutive_autoreply = Column(Integer, nullable=True)
    human_input_mode = Column(Enum("ALWAYS", "NEVER", "TERMINATE"), default="TERMINATE")
    function_map = Column(JSON, nullable=True)
    code_execution_config = Column(JSON, nullable=True)
    llm_config = Column(JSON, nullable=True)
    default_auto_reply = Column(Text, default="")
    description = Column(Text, nullable=True)
    chat_messages = Column(JSON, nullable=True)
    created_at = Column(TIMESTAMP, server_default=func.current_timestamp())


class AgentGroup(Base):
    __tablename__ = "agent_groups"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    created_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.current_timestamp(), nullable=False)
    updated_by = Column(Integer, ForeignKey('users.id'), nullable=True)
    updated_at = Column(TIMESTAMP, server_default=func.current_timestamp(), onupdate=func.current_timestamp(), nullable=True)
    max_round = Column(Integer, default=10)
    admin_name = Column(String, default="Admin")
    func_call_filter = Column(Boolean, default=True)
    speaker_selection_method = Column(
        String, default="auto"
    )  # This can be refined based on the specific method
    max_retries_for_selecting_speaker = Column(Integer, default=2)
    allow_repeat_speaker = Column(
        JSON, nullable=True
    )  # This can be a JSON field or specific type based on implementation
    allowed_or_disallowed_speaker_transitions = Column(JSON, nullable=True)
    speaker_transitions_type = Column(String, nullable=True)
    enable_clear_history = Column(Boolean, default=False)
    send_introductions = Column(Boolean, default=False)
    select_speaker_message_template = Column(
        Text,
        default="""You are in a role play game. The following roles are available:
                {roles}.
                Read the following conversation.
                Then select the next role from {agentlist} to play. Only return the role.""",
    )
    select_speaker_prompt_template = Column(
        Text,
        default="Read the above conversation. Then select the next role from {agentlist} to play. Only return the role.",
    )
    select_speaker_auto_multiple_template = Column(
        Text,
        default="""You provided more than one name in your text, please return just the name of the next speaker. To determine the speaker use these prioritised rules:
    1. If the context refers to themselves as a speaker e.g. "As the..." , choose that speaker's name
    2. If it refers to the "next" speaker name, choose that name
    3. Otherwise, choose the first provided speaker's name in the context
    The names are case-sensitive and should not be abbreviated or changed.
    Respond with ONLY the name of the speaker and DO NOT provide a reason. """,
    )
    select_speaker_auto_none_template = Column(
        Text,
        default="""You didn't choose a speaker. As a reminder, to determine the speaker use these prioritised rules:
    1. If the context refers to themselves as a speaker e.g. "As the..." , choose that speaker's name
    2. If it refers to the "next" speaker name, choose that name
    3. Otherwise, choose the first provided speaker's name in the context
    The names are case-sensitive and should not be abbreviated or changed.
    The only names that are accepted are {agentlist}.
    Respond with ONLY the name of the speaker and DO NOT provide a reason.""",
    )
    select_speaker_auto_verbose = Column(Boolean, nullable=True, default=False)
    role_for_select_speaker_messages = Column(String, nullable=True, default="system")


class AgentGroupMember(Base):
    __tablename__ = "agent_group_members"
    group_id = Column(
        Integer, ForeignKey("agent_groups.id"), primary_key=True, nullable=False
    )
    agent_id = Column(
        Integer, ForeignKey("agents.id"), primary_key=True, nullable=False
    )
    added_at = Column(TIMESTAMP, server_default=func.current_timestamp())


class AgentGroupMessage(Base):
    __tablename__ = "agent_group_messages"
    id = Column(Integer, primary_key=True, autoincrement=True)
    group_id = Column(Integer, ForeignKey("agent_groups.id"), nullable=False)
    sender_id = Column(Integer, ForeignKey("agents.id"), nullable=False)
    message = Column(JSON, nullable=False)
    sent_at = Column(TIMESTAMP, server_default=func.current_timestamp(), nullable=False)


# User
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)


# Post
class Post(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    content = Column(String)
    file_url = Column(String, nullable=True)
    user_id = Column(Integer, ForeignKey("users.id"))

    author = relationship("User")


# Chat
class ChatMessage(Base):
    __tablename__ = "chat_messages"
    id = Column(Integer, primary_key=True, index=True)
    message = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    recipient_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    timestamp = Column(DateTime, server_default=func.now())

    user = relationship("User", foreign_keys=[user_id])
    recipient = relationship("User", foreign_keys=[recipient_id])


# Session
class SessionModel(Base):
    __tablename__ = "sessions"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    session_data = Column(String)  # JSON or any other serialized format

    user = relationship("User")
