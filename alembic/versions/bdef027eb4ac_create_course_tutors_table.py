"""Create_Course_Tutors_table

Revision ID: bdef027eb4ac
Revises: bf9b588296e0
Create Date: 2022-12-09 10:41:49.517561

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bdef027eb4ac'
down_revision = 'bf9b588296e0'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('coursesTutors',
    sa.Column('ct_id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('tutor_id', sa.Integer(), nullable=False),
    sa.Column('course_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['course_id'], ['courses.course_id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['tutor_id'], ['tutors.tutor_id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('ct_id')
    )
    op.create_index(op.f('ix_coursesTutors_ct_id'), 'coursesTutors', ['ct_id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_coursesTutors_ct_id'), table_name='coursesTutors')
    op.drop_table('coursesTutors')
    # ### end Alembic commands ###
