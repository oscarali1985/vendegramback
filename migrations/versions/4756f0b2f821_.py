"""empty message

Revision ID: 4756f0b2f821
Revises: 
Create Date: 2020-09-24 15:22:27.730151

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4756f0b2f821'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('producto',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('titulo', sa.String(length=100), nullable=False),
    sa.Column('foto', sa.String(length=200), nullable=False),
    sa.Column('descripcion', sa.String(length=2000), nullable=False),
    sa.Column('precio', sa.Float(precision=10), nullable=False),
    sa.Column('cantidad', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('usuario',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('nombre', sa.String(length=50), nullable=False),
    sa.Column('apellido', sa.String(length=50), nullable=False),
    sa.Column('nombre_usuario', sa.String(length=20), nullable=False),
    sa.Column('fecha_nacimiento', sa.Date(), nullable=True),
    sa.Column('correo', sa.String(length=50), nullable=False),
    sa.Column('telefono', sa.String(length=20), nullable=False),
    sa.Column('clave_hash', sa.String(length=50), nullable=False),
    sa.Column('foto_perfil', sa.String(length=50), nullable=True),
    sa.Column('administrador', sa.Boolean(), nullable=False),
    sa.Column('suscripcion', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('correo'),
    sa.UniqueConstraint('nombre_usuario')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('usuario')
    op.drop_table('producto')
    # ### end Alembic commands ###
