"""Create_Students_Table

Revision ID: cd2edfdf4ce1
Revises: 70a4dc05e1aa
Create Date: 2022-10-22 17:45:34.666322

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cd2edfdf4ce1'
down_revision = '70a4dc05e1aa'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('students',
    sa.Column('student_id', sa.Integer(), nullable=False),
    sa.Column('full_name', sa.String(), nullable=True),
    sa.Column('full_name_arabic', sa.String(), nullable=True),
    sa.Column('student_image_id', sa.Integer(), nullable=True),
    sa.Column('colleage', sa.String(), nullable=False),
    sa.Column('year', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(), nullable=False),
    sa.Column('hashed_password', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('student_id'),
    sa.UniqueConstraint('student_image_id')
    )
    op.create_index(op.f('ix_students_email'), 'students', ['email'], unique=True)
    op.create_index(op.f('ix_students_full_name'), 'students', ['full_name'], unique=False)
    op.create_index(op.f('ix_students_full_name_arabic'), 'students', ['full_name_arabic'], unique=False)
    op.create_index(op.f('ix_students_student_id'), 'students', ['student_id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_students_student_id'), table_name='students')
    op.drop_index(op.f('ix_students_full_name_arabic'), table_name='students')
    op.drop_index(op.f('ix_students_full_name'), table_name='students')
    op.drop_index(op.f('ix_students_email'), table_name='students')
    op.drop_table('students')
    # ### end Alembic commands ###
