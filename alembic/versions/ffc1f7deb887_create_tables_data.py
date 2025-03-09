"""create tables data

Revision ID: ffc1f7deb887
Revises: 
Create Date: 2025-03-09 12:29:42.900792

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ffc1f7deb887'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('data_app',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('smoking_status', sa.Boolean(), nullable=True),
    sa.Column('caffeine_consumption', sa.Integer(), nullable=True),
    sa.Column('excercise_frecuency', sa.Integer(), nullable=True),
    sa.Column('alcohol_consumption', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_data_app_id'), 'data_app', ['id'], unique=False)
    op.create_table('smartwatch',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('sleep_duration', sa.Float(), nullable=False),
    sa.Column('rem_sleep_cycle', sa.Float(), nullable=False),
    sa.Column('deep_sleep_cycle', sa.Float(), nullable=False),
    sa.Column('light_sleep_cycle', sa.Float(), nullable=False),
    sa.Column('bedtime_hour', sa.Float(), nullable=False),
    sa.Column('awakenings', sa.Integer(), nullable=False),
    sa.Column('wakeup_hour', sa.Float(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_smartwatch_id'), 'smartwatch', ['id'], unique=False)
    op.create_table('user_type',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_type_id'), 'user_type', ['id'], unique=False)
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(length=100), nullable=False),
    sa.Column('password', sa.String(length=255), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('age', sa.Integer(), nullable=False),
    sa.Column('gender', sa.Boolean(), nullable=False),
    sa.Column('id_user_type', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['id_user_type'], ['user_type.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_id'), 'user', ['id'], unique=False)
    op.create_table('daily_report',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('id_user', sa.Integer(), nullable=False),
    sa.Column('id_data', sa.Integer(), nullable=False),
    sa.Column('id_smartwatch', sa.Integer(), nullable=False),
    sa.Column('date_daily', sa.Date(), nullable=True),
    sa.ForeignKeyConstraint(['id_data'], ['data_app.id'], ),
    sa.ForeignKeyConstraint(['id_smartwatch'], ['smartwatch.id'], ),
    sa.ForeignKeyConstraint(['id_user'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_daily_report_id'), 'daily_report', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_daily_report_id'), table_name='daily_report')
    op.drop_table('daily_report')
    op.drop_index(op.f('ix_user_id'), table_name='user')
    op.drop_table('user')
    op.drop_index(op.f('ix_user_type_id'), table_name='user_type')
    op.drop_table('user_type')
    op.drop_index(op.f('ix_smartwatch_id'), table_name='smartwatch')
    op.drop_table('smartwatch')
    op.drop_index(op.f('ix_data_app_id'), table_name='data_app')
    op.drop_table('data_app')
    # ### end Alembic commands ###
