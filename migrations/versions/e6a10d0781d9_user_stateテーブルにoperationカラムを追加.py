"""user_stateテーブルにoperationカラムを追加

Revision ID: e6a10d0781d9
Revises: 0dc60e8ffa7f
Create Date: 2023-09-16 14:23:30.832998

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e6a10d0781d9'
down_revision = '0dc60e8ffa7f'
branch_labels = None
depends_on = None


def upgrade():
    # 外部キー制約を削除
    op.drop_constraint('temp_event_user_id_fkey', 'temp_event', type_='foreignkey')

    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user_state', schema=None) as batch_op:
        batch_op.add_column(sa.Column('operation', sa.String(length=50), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user_state', schema=None) as batch_op:
        batch_op.drop_column('operation')

    # ### end Alembic commands ###
