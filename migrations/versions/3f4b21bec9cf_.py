"""empty message

Revision ID: 3f4b21bec9cf
Revises: 4846b199307b
Create Date: 2022-10-22 13:20:47.389444

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3f4b21bec9cf'
down_revision = '4846b199307b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('orders')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('orders',
    sa.Column('order_id', sa.INTEGER(), nullable=False),
    sa.Column('customer_id', sa.INTEGER(), nullable=True),
    sa.Column('email', sa.VARCHAR(length=64), nullable=True),
    sa.Column('address', sa.VARCHAR(length=128), nullable=True),
    sa.Column('items', sa.VARCHAR(length=256), nullable=True),
    sa.Column('amount', sa.INTEGER(), nullable=True),
    sa.PrimaryKeyConstraint('order_id')
    )
    # ### end Alembic commands ###
