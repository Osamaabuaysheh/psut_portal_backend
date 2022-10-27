"""Create_Events_Table

Revision ID: 61111895d2f6
Revises: 9b2d180289fc
Create Date: 2022-10-22 21:15:42.721647

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '61111895d2f6'
down_revision = '9b2d180289fc'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('Events',
    sa.Column('event_id', sa.Integer(), nullable=False),
    sa.Column('event_name', sa.String(), nullable=False),
    sa.Column('location', sa.String(), nullable=False),
    sa.Column('start_time', sa.Time(), nullable=False),
    sa.Column('end_time', sa.Time(), nullable=False),
    sa.Column('start_date', sa.Date(), nullable=False),
    sa.Column('end_date', sa.Date(), nullable=False),
    sa.Column('description', sa.String(), nullable=False),
    sa.Column('image', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('event_id')
    )
    op.create_index(op.f('ix_Events_event_id'), 'Events', ['event_id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_Events_event_id'), table_name='Events')
    op.drop_table('Events')
    # ### end Alembic commands ###