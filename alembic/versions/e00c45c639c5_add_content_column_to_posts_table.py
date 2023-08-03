"""add content column to posts table

Revision ID: e00c45c639c5
Revises: 942ba05edd00
Create Date: 2023-08-03 11:07:37.482477

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e00c45c639c5'
down_revision = '942ba05edd00'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))


def downgrade() -> None:
    op.drop_column('posts', 'content')
