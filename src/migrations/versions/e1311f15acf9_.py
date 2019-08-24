"""empty message

Revision ID: e1311f15acf9
Revises: c377fd754faa
Create Date: 2019-08-24 18:05:35.389394

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e1311f15acf9'
down_revision = 'c377fd754faa'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user_score', sa.Column('total', sa.Integer(), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user_score', 'total')
    # ### end Alembic commands ###
