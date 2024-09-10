"""Manual migration to fix schema

Revision ID: 9b876f737116
Revises: 22d09d7db165
Create Date: 2024-09-07 23:37:37.899919

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9b876f737116'
down_revision = '22d09d7db165'
branch_labels = None
depends_on = None


def upgrade():
    # Create a new table with the modified schema
    op.create_table(
        'product_new',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('price', sa.Float(), nullable=False),
        sa.Column('image', sa.String(length=100), nullable=True),  # Changed to nullable=True
        sa.Column('rating', sa.Integer(), nullable=True),
        sa.Column('category', sa.String(length=50), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )

    # Copy data from the old table to the new table
    op.execute('INSERT INTO product_new (id, name, price, image, rating, category) SELECT id, name, price, image, rating, category FROM product')

    # Drop the old table
    op.drop_table('product')

    # Rename the new table to the old table's name
    op.rename_table('product_new', 'product')


def downgrade():
    # Create the old table schema
    op.create_table(
        'product_old',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('price', sa.Float(), nullable=False),
        sa.Column('image', sa.String(length=100), nullable=False),  # Revert to not nullable
        sa.Column('rating', sa.Integer(), nullable=True),
        sa.Column('category', sa.String(length=50), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )

    # Copy data from the new table to the old table
    op.execute('INSERT INTO product_old (id, name, price, image, rating, category) SELECT id, name, price, image, rating, category FROM product')

    # Drop the new table
    op.drop_table('product')

    # Rename the old table to the new table's name
    op.rename_table('product_old', 'product')
