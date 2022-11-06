"""update user model

Revision ID: bb37329eb434
Revises: f338d43a1f28
Create Date: 2022-11-06 22:48:32.242354

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bb37329eb434'
down_revision = 'f338d43a1f28'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('is_admin', sa.Boolean(), nullable=False))
    op.drop_column('user', 'isAdmin')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('isAdmin', sa.BOOLEAN(), autoincrement=False, nullable=False))
    op.drop_column('user', 'is_admin')
    # ### end Alembic commands ###
