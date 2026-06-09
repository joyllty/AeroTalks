"""Adiciona creator_username em rooms

Revision ID: 7a3e5c9f1b2d
Revises: 484bdb7ddcd2
Create Date: 2026-06-09 20:20:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7a3e5c9f1b2d'
down_revision = '484bdb7ddcd2'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('rooms', sa.Column('creator_username', sa.String(length=50), nullable=True))


def downgrade():
    op.drop_column('rooms', 'creator_username')