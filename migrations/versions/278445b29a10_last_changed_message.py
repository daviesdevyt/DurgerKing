"""last_changed_message

Revision ID: 278445b29a10
Revises: 837bb9c1676f
Create Date: 2023-05-21 23:52:02.277617

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '278445b29a10'
down_revision = '837bb9c1676f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('last_changed_message', sa.DateTime(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'last_changed_message')
    # ### end Alembic commands ###