"""Make is_termination_msg nullable

Revision ID: 86f6413103f1
Revises: 07d1ff55542f
Create Date: 2024-06-28 10:19:59.987380

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import JSON
from enum import Enum

class AgentType(Enum):
    ConversableAgent = "ConversableAgent"
    UserProxyAgent = "UserProxyAgent"
    AssistantAgent = "AssistantAgent"
    
# revision identifiers, used by Alembic.
revision: str = '86f6413103f1'
down_revision: Union[str, None] = '07d1ff55542f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_table('agents')

    op.create_table(
        'agents',
        sa.Column('id', sa.Integer, primary_key=True, index=True, autoincrement=True),
        sa.Column('name', sa.String, nullable=False),
        sa.Column('user_id', sa.Integer, sa.ForeignKey("users.id"), nullable=False),
        sa.Column('agent_type', sa.Enum(AgentType), nullable=False),
        sa.Column('system_message', sa.String, default="You are a helpful AI Assistant."),
        sa.Column('is_termination_msg', sa.Text, nullable=True),
        sa.Column('max_consecutive_autoreply', sa.Integer, nullable=True),
        sa.Column('human_input_mode', sa.Enum("ALWAYS", "NEVER", "TERMINATE"), default="TERMINATE"),
        sa.Column('function_map', JSON, nullable=True),
        sa.Column('code_execution_config', JSON, nullable=True),
        sa.Column('llm_config', JSON, nullable=True),
        sa.Column('default_auto_reply', sa.Text, default=""),
        sa.Column('description', sa.Text, nullable=True),
        sa.Column('chat_messages', JSON, nullable=True),
        sa.Column('created_at', sa.TIMESTAMP, server_default=sa.func.current_timestamp()),
    )

def downgrade() -> None:
    op.drop_table('agents')

    op.create_table(
        'agents',
        sa.Column('id', sa.Integer, primary_key=True, index=True, autoincrement=True),
        sa.Column('name', sa.String, nullable=False),
        sa.Column('user_id', sa.Integer, sa.ForeignKey("users.id"), nullable=False),
        sa.Column('agent_type', sa.Enum(AgentType), nullable=False),
        sa.Column('system_message', sa.String, default="You are a helpful AI Assistant."),
        sa.Column('is_termination_msg', sa.Text, nullable=False),
        sa.Column('max_consecutive_autoreply', sa.Integer, nullable=True),
        sa.Column('human_input_mode', sa.Enum("ALWAYS", "NEVER", "TERMINATE"), default="TERMINATE"),
        sa.Column('function_map', JSON, nullable=True),
        sa.Column('code_execution_config', JSON, nullable=True),
        sa.Column('llm_config', JSON, nullable=True),
        sa.Column('default_auto_reply', sa.Text, default=""),
        sa.Column('description', sa.Text, nullable=True),
        sa.Column('chat_messages', JSON, nullable=True),
        sa.Column('created_at', sa.TIMESTAMP, server_default=sa.func.current_timestamp()),
    )