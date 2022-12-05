"""create_Clubs_table

Revision ID: f939809ecd61
Revises: 20a92eaca38d
Create Date: 2022-11-23 21:02:58.471834

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f939809ecd61'
down_revision = '20a92eaca38d'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('Clubs',
    sa.Column('club_id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('club_name', sa.String(), nullable=False),
    sa.Column('club_image', sa.String(), nullable=False),
    sa.Column('club_icon_image', sa.String(), nullable=False),
    sa.Column('description', sa.String(), nullable=False),
    sa.Column('link', sa.String(), nullable=False),
    sa.Column('contact_info', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('club_id', 'club_name')
    )
    op.create_index(op.f('ix_Clubs_club_id'), 'Clubs', ['club_id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_Clubs_club_id'), table_name='Clubs')
    op.drop_table('Clubs')
    # ### end Alembic commands ###