"""add donation

Revision ID: 407c94f41d90
Revises: 5d9125bb4d80
Create Date: 2024-12-05 13:28:25.812206

"""
import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = '407c94f41d90'
down_revision = '5d9125bb4d80'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('donation',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('comment', sa.Text(), nullable=True),
    sa.Column('full_amount', sa.Integer(), nullable=False),
    sa.Column('invested_amount', sa.Integer(), nullable=True),
    sa.Column('fully_invested', sa.Boolean(), nullable=True),
    sa.Column('create_date', sa.DateTime(), nullable=False),
    sa.Column('close_date', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('charityproject', schema=None) as batch_op:
        batch_op.alter_column('full_amount',
               existing_type=sa.INTEGER(),
               nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('charityproject', schema=None) as batch_op:
        batch_op.alter_column('full_amount',
               existing_type=sa.INTEGER(),
               nullable=True)

    op.drop_table('donation')
    # ### end Alembic commands ###
