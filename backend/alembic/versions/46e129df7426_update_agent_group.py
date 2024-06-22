"""update agent group

Revision ID: 46e129df7426
Revises: bea414eacf04
Create Date: 2024-06-22 12:10:37.990847

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '46e129df7426'
down_revision: Union[str, None] = 'bea414eacf04'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    with op.batch_alter_table('agent_groups', schema=None) as batch_op:
        batch_op.add_column(sa.Column('updated_by', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('updated_at', sa.TIMESTAMP(), server_default=sa.func.current_timestamp(), onupdate=sa.func.current_timestamp(), nullable=True))
        batch_op.add_column(sa.Column('max_round', sa.Integer(), nullable=False, server_default='10'))
        batch_op.add_column(sa.Column('admin_name', sa.String(), nullable=False, server_default='Admin'))
        batch_op.add_column(sa.Column('func_call_filter', sa.Boolean(), nullable=False, server_default='1'))
        batch_op.add_column(sa.Column('speaker_selection_method', sa.String(), nullable=False, server_default='auto'))
        batch_op.add_column(sa.Column('max_retries_for_selecting_speaker', sa.Integer(), nullable=False, server_default='2'))
        batch_op.add_column(sa.Column('allow_repeat_speaker', sa.JSON(), nullable=True))
        batch_op.add_column(sa.Column('allowed_or_disallowed_speaker_transitions', sa.JSON(), nullable=True))
        batch_op.add_column(sa.Column('speaker_transitions_type', sa.String(), nullable=True))
        batch_op.add_column(sa.Column('enable_clear_history', sa.Boolean(), nullable=False, server_default='0'))
        batch_op.add_column(sa.Column('send_introductions', sa.Boolean(), nullable=False, server_default='0'))
        batch_op.add_column(sa.Column('select_speaker_message_template', sa.Text(), nullable=False, server_default="""You are in a role play game. The following roles are available:
                {roles}.
                Read the following conversation.
                Then select the next role from {agentlist} to play. Only return the role."""))
        batch_op.add_column(sa.Column('select_speaker_prompt_template', sa.Text(), nullable=False, server_default="Read the above conversation. Then select the next role from {agentlist} to play. Only return the role."))
        batch_op.add_column(sa.Column('select_speaker_auto_multiple_template', sa.Text(), nullable=False, server_default="""You provided more than one name in your text, please return just the name of the next speaker. To determine the speaker use these prioritised rules:
    1. If the context refers to themselves as a speaker e.g. "As the..." , choose that speaker's name
    2. If it refers to the "next" speaker name, choose that name
    3. Otherwise, choose the first provided speaker's name in the context
    The names are case-sensitive and should not be abbreviated or changed.
    Respond with ONLY the name of the speaker and DO NOT provide a reason. """))
        batch_op.add_column(sa.Column('select_speaker_auto_none_template', sa.Text(), nullable=False, server_default="""You didn't choose a speaker. As a reminder, to determine the speaker use these prioritised rules:
    1. If the context refers to themselves as a speaker e.g. "As the..." , choose that speaker's name
    2. If it refers to the "next" speaker name, choose that name
    3. Otherwise, choose the first provided speaker's name in the context
    The names are case-sensitive and should not be abbreviated or changed.
    The only names that are accepted are {agentlist}.
    Respond with ONLY the name of the speaker and DO NOT provide a reason."""))
        batch_op.add_column(sa.Column('select_speaker_auto_verbose', sa.Boolean(), nullable=True, server_default='0'))
        batch_op.add_column(sa.Column('role_for_select_speaker_messages', sa.String(), nullable=True, server_default='system'))


def downgrade():
    with op.batch_alter_table('agent_groups', schema=None) as batch_op:
        batch_op.drop_column('updated_by')
        batch_op.drop_column('updated_at')
        batch_op.drop_column('max_round')
        batch_op.drop_column('admin_name')
        batch_op.drop_column('func_call_filter')
        batch_op.drop_column('speaker_selection_method')
        batch_op.drop_column('max_retries_for_selecting_speaker')
        batch_op.drop_column('allow_repeat_speaker')
        batch_op.drop_column('allowed_or_disallowed_speaker_transitions')
        batch_op.drop_column('speaker_transitions_type')
        batch_op.drop_column('enable_clear_history')
        batch_op.drop_column('send_introductions')
        batch_op.drop_column('select_speaker_message_template')
        batch_op.drop_column('select_speaker_prompt_template')
        batch_op.drop_column('select_speaker_auto_multiple_template')
        batch_op.drop_column('select_speaker_auto_none_template')
        batch_op.drop_column('select_speaker_auto_verbose')
        batch_op.drop_column('role_for_select_speaker_messages')
