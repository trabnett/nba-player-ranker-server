"""ip_address
Revision ID: f9a6dd0d1b86
Revises: 243b16e113f3
Create Date: 2019-04-29 11:24:20.938891
"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f9a6dd0d1b86'
down_revision = '243b16e113f3'
branch_labels = None
depends_on = None


def upgrade():
    return None
    # ### commands auto generated by Alembic - please adjust! ###
    # op.create_table('IP',
    # sa.Column('id', sa.Integer(), nullable=False),
    # sa.Column('ip_address', sa.String(length=140), nullable=True),
    # sa.Column('timestamp', sa.DateTime(), nullable=True),
    # sa.Column('count', sa.Integer(), nullable=True),
    # sa.PrimaryKeyConstraint('id')
    # )
    # op.create_index(op.f('ix_IP_timestamp'), 'IP', ['timestamp'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    return None
    # ### commands auto generated by Alembic - please adjust! ###
    # op.drop_index(op.f('ix_IP_timestamp'), table_name='IP')
    # op.drop_table('IP')
    # ### end Alembic commands ###