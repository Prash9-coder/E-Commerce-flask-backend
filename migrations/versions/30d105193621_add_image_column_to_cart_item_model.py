"""Add image column to cart_item model

Revision ID: 30d105193621
Revises: 9b876f737116
Create Date: 2024-09-08 00:10:34.175750

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '30d105193621'
down_revision = '9b876f737116'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('cart_item', schema=None) as batch_op:
        batch_op.add_column(sa.Column('image', sa.String(length=120), nullable=True))

    with op.batch_alter_table('product', schema=None) as batch_op:
        batch_op.alter_column('image',
               existing_type=sa.VARCHAR(length=100),
               nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('product', schema=None) as batch_op:
        batch_op.alter_column('image',
               existing_type=sa.VARCHAR(length=100),
               nullable=True)

    with op.batch_alter_table('cart_item', schema=None) as batch_op:
        batch_op.drop_column('image')

    # ### end Alembic commands ###
