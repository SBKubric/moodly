"""empty message

Revision ID: 269279e18cdb
Revises: 
Create Date: 2020-02-02 19:40:33.518147

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '269279e18cdb'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('post',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('reddit_id', sa.String(length=50), nullable=True),
    sa.Column('body', sa.Text(), nullable=True),
    sa.Column('url', sa.String(length=150), nullable=True),
    sa.Column('done', sa.Boolean(), nullable=True),
    sa.Column('score', sa.Float(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('settings',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=50), nullable=True),
    sa.Column('name', sa.String(length=50), nullable=True),
    sa.Column('value', sa.String(length=50), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=50), nullable=True),
    sa.Column('password', sa.String(length=128), nullable=True),
    sa.Column('role', sa.String(length=10), nullable=True),
    sa.Column('email', sa.String(length=50), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    op.create_index(op.f('ix_user_role'), 'user', ['role'], unique=False)
    op.create_index(op.f('ix_user_username'), 'user', ['username'], unique=True)
    op.create_table('comment',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('reddit_id', sa.String(length=50), nullable=True),
    sa.Column('body', sa.Text(), nullable=True),
    sa.Column('url', sa.String(length=150), nullable=True),
    sa.Column('author', sa.String(length=50), nullable=True),
    sa.Column('score', sa.Float(), nullable=True),
    sa.Column('post_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['post_id'], ['post.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('query',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('category_id', sa.Integer(), nullable=True),
    sa.Column('query_str', sa.String(length=50), nullable=True),
    sa.Column('age_id', sa.Integer(), nullable=True),
    sa.Column('status', sa.String(length=25), nullable=True),
    sa.Column('percent', sa.Integer(), nullable=True),
    sa.Column('result_url', sa.String(length=12), nullable=True),
    sa.Column('date', sa.DateTime(), nullable=True),
    sa.Column('user', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['age_id'], ['settings.id'], ),
    sa.ForeignKeyConstraint(['category_id'], ['settings.id'], ),
    sa.ForeignKeyConstraint(['user'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_query_result_url'), 'query', ['result_url'], unique=True)
    op.create_table('association',
    sa.Column('query_id', sa.Integer(), nullable=True),
    sa.Column('post_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['post_id'], ['post.id'], ),
    sa.ForeignKeyConstraint(['query_id'], ['query.id'], )
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('association')
    op.drop_index(op.f('ix_query_result_url'), table_name='query')
    op.drop_table('query')
    op.drop_table('comment')
    op.drop_index(op.f('ix_user_username'), table_name='user')
    op.drop_index(op.f('ix_user_role'), table_name='user')
    op.drop_table('user')
    op.drop_table('settings')
    op.drop_table('post')
    # ### end Alembic commands ###
