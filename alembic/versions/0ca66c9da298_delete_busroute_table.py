"""Delete busRoute Table

Revision ID: 0ca66c9da298
Revises: a8df0d6c505e
Create Date: 2022-12-25 19:25:35.618769

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0ca66c9da298'
down_revision = 'a8df0d6c505e'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('ix_BusRoutes_bus_route_id', table_name='BusRoutes')
    op.drop_table('BusRoutes')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('BusRoutes',
    sa.Column('bus_route_id', sa.INTEGER(), server_default=sa.text('nextval(\'"BusRoutes_bus_route_id_seq"\'::regclass)'), autoincrement=True, nullable=False),
    sa.Column('bus_route_name', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('first_route', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('second_route', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('third_route', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('fourth_route', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('location_trip', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('bus_route_id', name='BusRoutes_pkey')
    )
    op.create_index('ix_BusRoutes_bus_route_id', 'BusRoutes', ['bus_route_id'], unique=False)
    # ### end Alembic commands ###
