"""describe the changes

Revision ID: 0dc60e8ffa7f
Revises: d1df9ac13b28
Create Date: 2023-09-16 10:52:34.493989

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0dc60e8ffa7f'
down_revision = 'd1df9ac13b28'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('temp_line_id',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('line_id', sa.String(length=255), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('line_id')
    )

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('temp_line_id')
    # ### end Alembic commands ###
