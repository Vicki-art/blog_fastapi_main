"""add user table

Revision ID: 1215a414cd9a
Revises: 7e1526dde8e1
Create Date: 2024-03-08 15:00:49.843631

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1215a414cd9a'
down_revision = '7e1526dde8e1'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('users',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('email', sa.String(), nullable=False),
                    sa.Column('password', sa.String(), nullable=False),
                    sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('email'))


def downgrade() -> None:
    op.drop_table('users')
