from pydantic import BaseModel
from typing import List, Optional, Union, Dict
from datetime import datetime
from enum import Enum as PydanticEnum

# Agent Group Chat related

class AgentTypeEnum(str, PydanticEnum):
    ConversableAgent = "ConversableAgent"
    UserProxyAgent = "UserProxyAgent"
    AssistantAgent = "AssistantAgent"

class AIAgentBase(BaseModel):
    name: str
    user_id: int
    agent_type: AgentTypeEnum
    system_message: Optional[str] = "You are a helpful AI Assistant."
    is_termination_msg: Optional[str] = None
    max_consecutive_autoreply: Optional[int] = None
    human_input_mode: Optional[str] = "TERMINATE"
    function_map: Optional[Dict[str, str]] = None
    code_execution_config: Optional[Dict] = None
    llm_config: Optional[Dict] = None
    default_auto_reply: Optional[str] = ""
    description: Optional[str] = None
    chat_messages: Optional[Dict[str, List[Dict]]] = None

class AIAgentCreate(AIAgentBase):
    pass

class AIAgent(AIAgentBase):
    id: int
    created_at: Optional[str]

    class Config:
        orm_mode = True

class AIAgentUpdate(BaseModel):
    name: Optional[str]
    agent_type: Optional[AgentTypeEnum]
    system_message: Optional[str]
    is_termination_msg: Optional[str]
    max_consecutive_autoreply: Optional[int]
    human_input_mode: Optional[str]
    function_map: Optional[Dict[str, str]]
    code_execution_config: Optional[Dict[str, str]]
    llm_config: Optional[Dict[str, str]]
    default_auto_reply: Optional[str]
    description: Optional[str]
    chat_messages: Optional[Dict[str, List[Dict[str, Union[str, int]]]]]

class AgentGroupBase(BaseModel):
    name: str
    created_by: int
    manager_id: int
    creator_user_proxy_id: int

class AgentGroupCreate(AgentGroupBase):
    pass

class AgentGroup(AgentGroupBase):
    id: int
    created_at: Optional[str]

    class Config:
        orm_mode = True

class AIAgent(AIAgentBase):
    id: int
    created_at: Optional[str]

    class Config:
        orm_mode = True

class AgentGroupUpdate(BaseModel):
    name: Optional[str]
    manager_id: Optional[int]
    creator_user_proxy_id: Optional[int]
        
class AgentGroupMemberBase(BaseModel):
    group_id: int
    agent_id: int

class AgentGroupMemberCreate(AgentGroupMemberBase):
    pass

class AgentGroupMember(AgentGroupMemberBase):
    added_at: Optional[str]

    class Config:
        orm_mode = True
        

class AgentGroupMessageBase(BaseModel):
    group_id: int
    sender_id: int
    message: str

class AgentGroupMessageCreate(AgentGroupMessageBase):
    pass
    
class AgentGroupMessageUpdate(BaseModel):
    sender_id: Optional[int]
    message: Optional[str]

class AgentGroupMessage(AgentGroupMessageBase):
    id: int
    sent_at: Optional[str]

    class Config:
        orm_mode = True


# User
class UserBase(BaseModel):
    name: str
    email: str

class UserCreate(UserBase):
    pass

class UserUpdate(BaseModel):
    name: str
    email: str

class User(UserBase):
    id: int

    class Config:
        orm_mode = True

# Post
class PostBase(BaseModel):
    title: str
    content: str
    file_url: Optional[str] = None

class PostCreate(PostBase):
    user_id: int

class PostUpdate(PostBase):
    pass

class Post(PostBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True

# ChatMessage
class ChatMessageBase(BaseModel):
    user_id: int
    message: str
    recipient_id: Optional[int] = None
    
class ChatMessageCreate(ChatMessageBase):
    pass
    
class ChatMessage(ChatMessageBase):
    id: int
    timestamp: datetime
    
    class Config:
        orm_mode = True