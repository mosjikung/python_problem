"""add product status

Revision ID: f061b9fa59b3
Revises: aca06e94c87f
Create Date: 2023-03-10 22:11:30.624978

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f061b9fa59b3'
down_revision = 'aca06e94c87f'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('product_status',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('status_name', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.add_column('product', sa.Column('product_status_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'product', 'product_status', ['product_status_id'], ['id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'product', type_='foreignkey')
    op.drop_column('product', 'product_status_id')
    op.drop_table('product_status')
    # ### end Alembic commands ###
