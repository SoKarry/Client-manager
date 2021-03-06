"""leadsv2.0 table

Revision ID: 367d5224e02e
Revises: 75d92a19e35b
Create Date: 2020-04-23 13:17:40.809395

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '367d5224e02e'
down_revision = '75d92a19e35b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('lead', schema=None) as batch_op:
        batch_op.add_column(sa.Column('contact', sa.String(length=90), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('lead', schema=None) as batch_op:
        batch_op.drop_column('contact')

    # ### end Alembic commands ###
