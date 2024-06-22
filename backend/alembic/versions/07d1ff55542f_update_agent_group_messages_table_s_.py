"""update agent_group_messages table's message column type to JSON

Revision ID: 07d1ff55542f
Revises: 46e129df7426
Create Date: 2024-06-22 20:58:13.545061

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '07d1ff55542f'
down_revision: Union[str, None] = '46e129df7426'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    with op.batch_alter_table('agent_group_messages', schema=None) as batch_op:
        batch_op.alter_column('message', existing_type=sa.Text(), type_=sa.JSON(), nullable=False)
        batch_op.alter_column('sent_at', existing_type=sa.TIMESTAMP(), nullable=False, server_default=sa.func.current_timestamp())


def downgrade():
    with op.batch_alter_table('agent_group_messages', schema=None) as batch_op:
        batch_op.alter_column('message', existing_type=sa.JSON(), type_=sa.Text(), nullable=False)
        batch_op.alter_column('sent_at', existing_type=sa.TIMESTAMP(), nullable=True, server_default=None)