"""empty message

Revision ID: c377fd754faa
Revises: 1d2c21b7f823
Create Date: 2019-08-24 17:13:57.704770

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c377fd754faa'
down_revision = '1d2c21b7f823'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('channel_score',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('daily_average', sa.Integer(), nullable=False),
    sa.Column('date', sa.Date(), nullable=False),
    sa.Column('cid', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['cid'], ['channel.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user_score',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('daily_average', sa.Integer(), nullable=False),
    sa.Column('date', sa.Date(), nullable=False),
    sa.Column('uid', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['uid'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('score')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('score',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('daily_average', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('date', sa.DATE(), autoincrement=False, nullable=False),
    sa.Column('uid', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('cid', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['cid'], ['channel.id'], name='score_cid_fkey'),
    sa.ForeignKeyConstraint(['uid'], ['user.id'], name='score_uid_fkey'),
    sa.PrimaryKeyConstraint('id', name='score_pkey')
    )
    op.drop_table('user_score')
    op.drop_table('channel_score')
    # ### end Alembic commands ###
