"""イントからストリングに変更

Revision ID: f26c853e763a
Revises: 08027f8e3d40
Create Date: 2023-09-26 20:18:07.811821

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f26c853e763a'
down_revision = '08027f8e3d40'
branch_labels = None
depends_on = None


def upgrade():
    # 外部キー制約を削除
    op.drop_constraint('event_user_id_fkey', 'event', type_='foreignkey')
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('event', schema=None) as batch_op:
        batch_op.alter_column('user_id',
               existing_type=sa.INTEGER(),
               type_=sa.String(length=255),
               existing_nullable=False)

    with op.batch_alter_table('user_state', schema=None) as batch_op:
        batch_op.alter_column('user_id',
               existing_type=sa.INTEGER(),
               type_=sa.String(length=255),
               existing_nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user_state', schema=None) as batch_op:
        batch_op.alter_column('user_id',
               existing_type=sa.String(length=255),
               type_=sa.INTEGER(),
               existing_nullable=False)

    with op.batch_alter_table('event', schema=None) as batch_op:
        batch_op.alter_column('user_id',
               existing_type=sa.String(length=255),
               type_=sa.INTEGER(),
               existing_nullable=False)

    # ### end Alembic commands ###
