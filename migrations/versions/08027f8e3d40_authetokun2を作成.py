"""AutheTokun2を作成

Revision ID: 08027f8e3d40
Revises: e906da531683
Create Date: 2023-09-26 19:28:21.143262

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '08027f8e3d40'
down_revision = 'e906da531683'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('auth_token2',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('line_id', sa.String(), nullable=False),
    sa.Column('token', sa.String(), nullable=False),
    sa.Column('gmail_address', sa.String(), nullable=True),
    sa.Column('expiration_time', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('line_id'),
    sa.UniqueConstraint('token')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('auth_token2')
    # ### end Alembic commands ###
