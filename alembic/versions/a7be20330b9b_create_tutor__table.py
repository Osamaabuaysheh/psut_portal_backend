"""create_Tutor__Table

Revision ID: a7be20330b9b
Revises: df5fd5d2e091
Create Date: 2022-11-29 07:47:14.722339

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a7be20330b9b'
down_revision = 'df5fd5d2e091'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('tutors',
    sa.Column('tutor_id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('tutor_name', sa.String(), nullable=False),
    sa.Column('gpa', sa.Float(), nullable=False),
    sa.Column('year', sa.Integer(), nullable=False),
    sa.Column('owner_id', sa.Integer(), nullable=False),
    sa.Column('student_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['owner_id'], ['users.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['student_id'], ['students.student_id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('tutor_id')
    )
    op.create_index(op.f('ix_tutors_tutor_id'), 'tutors', ['tutor_id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_tutors_tutor_id'), table_name='tutors')
    op.drop_table('tutors')
    # ### end Alembic commands ###