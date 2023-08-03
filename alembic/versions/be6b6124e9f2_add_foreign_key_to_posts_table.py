"""add foreign key to posts table

Revision ID: be6b6124e9f2
Revises: 52d8b2cb5733
Create Date: 2023-08-03 11:19:46.996955

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'be6b6124e9f2'
down_revision = '52d8b2cb5733'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('owner_id', sa.Integer(), nullable=False))
    op.create_foreign_key("posts_users_fk", source_table='posts', referent_table='users', local_cols=['owner_id'], remote_cols=['id'], ondelete='CASCADE')
    pass


def downgrade() -> None:
    op.drop_constraint('posts_users_fk', table_name="posts")
    op.drop_column('posts', 'owner_id')
    pass

