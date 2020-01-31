"""empty message

Revision ID: 0c31120a1d48
Revises: 52c22cf76462
Create Date: 2020-02-01 01:14:37.556264

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0c31120a1d48'
down_revision = '52c22cf76462'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('post', sa.Column('done', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('post', 'done')
    # ### end Alembic commands ###
