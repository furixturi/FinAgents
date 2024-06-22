from pydantic import BaseModel
from typing import List, Optional, Union, Dict, Literal
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
    max_round: Optional[int] = 10
    admin_name: Optional[str] = "Admin"
    func_call_filter: Optional[bool] = True
    speaker_selection_method: Optional[
        Union[str, Literal["auto", "manual", "random", "round_robin"]]
    ] = "auto"
    max_retries_for_selecting_speaker: Optional[int] = 2
    allow_repeat_speaker: Optional[Union[bool, List[int]]] = None
    allowed_or_disallowed_speaker_transitions: Optional[Dict] = None
    speaker_transitions_type: Optional[Union[str, Literal["allowed", "disallowed"]]] = (
        None
    )
    enable_clear_history: Optional[bool] = False
    send_introductions: Optional[bool] = False
    select_speaker_message_template: Optional[
        str
    ] = """You are in a role play game. The following roles are available:
                {roles}.
                Read the following conversation.
                Then select the next role from {agentlist} to play. Only return the role."""
    select_speaker_prompt_template: Optional[str] = (
        "Read the above conversation. The select the next role from {agentlist} to play. Only return the role."
    )
    select_speaker_auto_multiple_template: Optional[
        str
    ] = """You provided more than one name in your text, please return just the name of the next speaker. To determine the speaker use these prioritised rules:
    1. If the context refers to themselves as a speaker e.g. "As the..." , choose that speaker's name
    2. If it refers to the "next" speaker name, choose that name
    3. Otherwise, choose the first provided speaker's name in the context
    The names are case-sensitive and should not be abbreviated or changed.
    Respond with ONLY the name of the speaker and DO NOT provide a reason."""
    select_speaker_auto_none_template: Optional[
        str
    ] = """You didn't choose a speaker. As a reminder, to determine the speaker use these prioritised rules:
    1. If the context refers to themselves as a speaker e.g. "As the..." , choose that speaker's name
    2. If it refers to the "next" speaker name, choose that name
    3. Otherwise, choose the first provided speaker's name in the context
    The names are case-sensitive and should not be abbreviated or changed.
    The only names that are accepted are {agentlist}.
    Respond with ONLY the name of the speaker and DO NOT provide a reason."""
    select_speaker_auto_verbose: Optional[bool] = False
    role_for_select_speaker_messages: Optional[str] = "system"


class AgentGroupCreate(AgentGroupBase):
    created_by: int

class AgentGroupUpdate(BaseModel):
    name: Optional[str]
    max_round: Optional[int]
    admin_name: Optional[str]
    func_call_filter: Optional[bool]
    speaker_selection_method: Optional[Union[str, Literal['auto', 'manual', 'random', 'round_robin']]]
    max_retries_for_selecting_speaker: Optional[int]
    allow_repeat_speaker: Optional[Union[bool, List[int]]]
    allowed_or_disallowed_speaker_transitions: Optional[Dict]
    speaker_transitions_type: Optional[Union[str, Literal['allowed', 'disallowed']]]
    enable_clear_history: Optional[bool]
    send_introductions: Optional[bool]
    select_speaker_message_template: Optional[str]
    select_speaker_prompt_template: Optional[str]
    select_speaker_auto_multiple_template: Optional[str]
    select_speaker_auto_none_template: Optional[str]
    select_speaker_auto_verbose: Optional[bool]
    role_for_select_speaker_messages: Optional[str]

class AgentGroup(AgentGroupBase):
    id: int
    created_by: int
    created_at: str
    updated_by: Optional[int]
    updated_at: Optional[str]

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
