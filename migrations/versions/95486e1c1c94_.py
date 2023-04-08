"""empty message

Revision ID: 95486e1c1c94
Revises: 9b902e807c89
Create Date: 2023-04-08 11:05:35.490145

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '95486e1c1c94'
down_revision = '9b902e807c89'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('id', sa.BigInteger(), nullable=False))
    op.drop_column('user', 'uid')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('uid', sa.INTEGER(), autoincrement=True, nullable=False))
    op.drop_column('user', 'id')
    # ### end Alembic commands ###