"""fixing table

Revision ID: 818c1076917d
Revises: 182c677ebc7b
Create Date: 2020-04-23 11:25:35.863945

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '818c1076917d'
down_revision = '182c677ebc7b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('client', 'cost_price',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.alter_column('client', 'price',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.alter_column('client', 'profit',
               existing_type=sa.INTEGER(),
               nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('client', 'profit',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.alter_column('client', 'price',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.alter_column('client', 'cost_price',
               existing_type=sa.INTEGER(),
               nullable=False)
    # ### end Alembic commands ###