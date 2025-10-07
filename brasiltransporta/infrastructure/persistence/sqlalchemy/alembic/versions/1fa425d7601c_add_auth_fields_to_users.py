"""add auth fields to users

Revision ID: 1fa425d7601c
Revises: 3865f805473e
Create Date: 2024-01-01 10:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '1fa425d7601c'
down_revision = '3865f805473e'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Adicionar novos campos de autenticação
    op.add_column('users', sa.Column('phone', sa.String(length=20), nullable=True))
    op.add_column('users', sa.Column('birth_date', sa.String(length=10), nullable=True))
    op.add_column('users', sa.Column('profession', sa.String(length=100), nullable=True))
    op.add_column('users', sa.Column('roles', postgresql.JSON(astext_type=sa.Text()), nullable=False, server_default='[]'))
    op.add_column('users', sa.Column('is_active', sa.Boolean(), nullable=False, server_default='true'))
    op.add_column('users', sa.Column('is_verified', sa.Boolean(), nullable=False, server_default='false'))
    op.add_column('users', sa.Column('last_login', sa.DateTime(timezone=True), nullable=True))


def downgrade() -> None:
    # Remover os campos adicionados
    op.drop_column('users', 'last_login')
    op.drop_column('users', 'is_verified')
    op.drop_column('users', 'is_active')
    op.drop_column('users', 'roles')
    op.drop_column('users', 'profession')
    op.drop_column('users', 'birth_date')
    op.drop_column('users', 'phone')
