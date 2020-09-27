"""empty message

Revision ID: f5b11533d7a9
Revises: 
Create Date: 2020-09-23 21:44:18.440643

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f5b11533d7a9'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('producto',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('titulo', sa.String(length=50), nullable=False),
    sa.Column('foto', sa.String(length=50), nullable=False),
    sa.Column('descripcion', sa.String(length=200), nullable=False),
    sa.Column('precio', sa.Float(precision=50), nullable=False),
    sa.Column('cantidad', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('producto')
    # ### end Alembic commands ###
