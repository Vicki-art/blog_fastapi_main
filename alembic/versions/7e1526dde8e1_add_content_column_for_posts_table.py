"""add content column for posts table

Revision ID: 7e1526dde8e1
Revises: 73fa2478a818
Create Date: 2024-03-08 14:55:35.135228

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7e1526dde8e1'
down_revision = '73fa2478a818'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))


def downgrade() -> None:
    op.drop_column('posts', 'content')
