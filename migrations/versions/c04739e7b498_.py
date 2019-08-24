"""empty message

Revision ID: c04739e7b498
Revises: e881b86e5483
Create Date: 2019-08-24 11:32:58.089505

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c04739e7b498'
down_revision = 'e881b86e5483'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('score',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('daily_average', sa.Integer(), nullable=False),
    sa.Column('date', sa.Date(), nullable=False),
    sa.Column('name', sa.Text(), nullable=False),
    sa.Column('channel', sa.Text(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('user')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('average_postive', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('average_neutral', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('average_negative', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('id', name='user_pkey')
    )
    op.drop_table('score')
    # ### end Alembic commands ###