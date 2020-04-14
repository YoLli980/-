"""empty message

Revision ID: ac7be2877a46
Revises: 
Create Date: 2019-12-04 09:10:26.021065

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ac7be2877a46'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('root',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('num', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=4), nullable=False),
    sa.Column('password', sa.String(length=25), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id')
    )
    op.create_table('student',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('num', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=4), nullable=False),
    sa.Column('major', sa.String(length=20), nullable=False),
    sa.Column('grade', sa.String(length=20), nullable=False),
    sa.Column('college', sa.String(length=30), nullable=False),
    sa.Column('password', sa.String(length=30), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id'),
    sa.UniqueConstraint('num')
    )
    op.create_table('teacher',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('num', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=4), nullable=False),
    sa.Column('college', sa.String(length=30), nullable=False),
    sa.Column('password', sa.String(length=30), nullable=False),
    sa.Column('is_root', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id'),
    sa.UniqueConstraint('num')
    )
    op.create_table('schedule',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=30), nullable=False),
    sa.Column('major', sa.String(length=30), nullable=False),
    sa.Column('classes', sa.String(length=30), nullable=False),
    sa.Column('college', sa.String(length=30), nullable=False),
    sa.Column('teacher_id', sa.Integer(), nullable=True),
    sa.Column('grade', sa.String(length=30), nullable=False),
    sa.Column('random_code', sa.String(length=30), nullable=False),
    sa.Column('trem', sa.Date(), nullable=True),
    sa.ForeignKeyConstraint(['teacher_id'], ['teacher.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id')
    )
    op.create_index(op.f('ix_schedule_trem'), 'schedule', ['trem'], unique=False)
    op.create_table('class_know',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('schedule_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['schedule_id'], ['schedule.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id')
    )
    op.create_table('curricula_variable',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('schedule_id', sa.Integer(), nullable=True),
    sa.Column('student_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['schedule_id'], ['schedule.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['student_id'], ['student.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id')
    )
    op.create_table('tmp_curricula',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('schedule_id', sa.Integer(), nullable=True),
    sa.Column('student_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['schedule_id'], ['schedule.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['student_id'], ['student.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id')
    )
    op.create_table('proficiency',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('proficiency', sa.String(length=50), nullable=True),
    sa.Column('estimate', sa.String(length=50), nullable=True),
    sa.Column('class_know_id', sa.Integer(), nullable=True),
    sa.Column('student_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['class_know_id'], ['class_know.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['student_id'], ['student.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('proficiency')
    op.drop_table('tmp_curricula')
    op.drop_table('curricula_variable')
    op.drop_table('class_know')
    op.drop_index(op.f('ix_schedule_trem'), table_name='schedule')
    op.drop_table('schedule')
    op.drop_table('teacher')
    op.drop_table('student')
    op.drop_table('root')
    # ### end Alembic commands ###
