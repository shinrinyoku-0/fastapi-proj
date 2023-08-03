"""create posts table

Revision ID: 942ba05edd00
Revises: 
Create Date: 2023-08-03 11:02:29.738006

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '942ba05edd00'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('posts', 
                    sa.Column('id', sa.Integer(), nullable=False, primary_key=True), 
                    sa.Column('title', sa.String(), nullable=False))
    pass

def downgrade() -> None:
    op.drop_table('posts')
    pass
