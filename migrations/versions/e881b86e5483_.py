"""empty message

Revision ID: e881b86e5483
Revises: 
Create Date: 2019-08-24 07:40:18.074706

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e881b86e5483'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('average_postive', sa.Integer(), nullable=False),
    sa.Column('average_neutral', sa.Integer(), nullable=False),
    sa.Column('average_negative', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user')
    # ### end Alembic commands ###
