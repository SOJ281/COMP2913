"""empty message

Revision ID: c194b5061ebf
Revises: a4b9c43bb6df
Create Date: 2022-03-12 12:39:23.849361

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c194b5061ebf'
down_revision = 'a4b9c43bb6df'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('bookings', schema=None) as batch_op:
        batch_op.add_column(sa.Column('completed', sa.Integer(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('bookings', schema=None) as batch_op:
        batch_op.drop_column('completed')

    # ### end Alembic commands ###
