"""Description of the changes

Revision ID: 624cd87c740e
Revises: 30d105193621
Create Date: 2024-09-08 10:41:09.113386

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '624cd87c740e'
down_revision = '30d105193621'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('cart_item', schema=None) as batch_op:
        batch_op.drop_column('image')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('cart_item', schema=None) as batch_op:
        batch_op.add_column(sa.Column('image', sa.VARCHAR(length=120), nullable=True))

    # ### end Alembic commands ###
