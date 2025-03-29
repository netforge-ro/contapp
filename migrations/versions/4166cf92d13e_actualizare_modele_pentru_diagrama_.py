"""Actualizare modele pentru diagrama relationala

Revision ID: 4166cf92d13e
Revises: 
Create Date: 2025-03-29 16:53:55.846789

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4166cf92d13e'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('facturi', schema=None) as batch_op:
        batch_op.add_column(sa.Column('data_factura', sa.Date(), nullable=False))
        batch_op.add_column(sa.Column('serie_factura', sa.String(length=10), nullable=False))
        batch_op.add_column(sa.Column('nr_factura', sa.Integer(), nullable=False))
        batch_op.add_column(sa.Column('valoare', sa.Numeric(precision=10, scale=2), nullable=False))
        batch_op.add_column(sa.Column('modalitate_plata', sa.String(length=50), nullable=True))
        batch_op.add_column(sa.Column('furnizor_id', sa.Integer(), nullable=False))
        batch_op.alter_column('valoare_tva',
               existing_type=sa.NUMERIC(precision=10, scale=2),
               nullable=True)
        batch_op.alter_column('client_id',
               existing_type=sa.INTEGER(),
               nullable=True)
        batch_op.drop_constraint('uix_serie_numar', type_='unique')
        batch_op.create_unique_constraint('uix_serie_numar', ['serie_factura', 'nr_factura'])
        batch_op.create_foreign_key(None, 'furnizori', ['furnizor_id'], ['id'])
        batch_op.drop_column('data_emitere')
        batch_op.drop_column('achitata')
        batch_op.drop_column('metoda_plata')
        batch_op.drop_column('valoare_totala')
        batch_op.drop_column('numar')
        batch_op.drop_column('serie')

    with op.batch_alter_table('furnizori', schema=None) as batch_op:
        batch_op.add_column(sa.Column('cod_fiscal', sa.String(length=20), nullable=True))
        batch_op.add_column(sa.Column('cont_bancar', sa.String(length=50), nullable=True))
        batch_op.add_column(sa.Column('sold_furnizor', sa.Numeric(precision=10, scale=2), nullable=True))
        batch_op.drop_column('judet')
        batch_op.drop_column('email')
        batch_op.drop_column('oras')

    with op.batch_alter_table('miscari_stoc', schema=None) as batch_op:
        batch_op.add_column(sa.Column('comanda_id', sa.Integer(), nullable=True))
        batch_op.create_foreign_key(None, 'comenzi', ['comanda_id'], ['id'])

    with op.batch_alter_table('produse', schema=None) as batch_op:
        batch_op.add_column(sa.Column('pret', sa.Numeric(precision=10, scale=2), nullable=True))
        batch_op.alter_column('pret_achizitie',
               existing_type=sa.NUMERIC(precision=10, scale=2),
               nullable=True)
        batch_op.alter_column('pret_vanzare',
               existing_type=sa.NUMERIC(precision=10, scale=2),
               nullable=True)
        batch_op.drop_column('descriere')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('produse', schema=None) as batch_op:
        batch_op.add_column(sa.Column('descriere', sa.TEXT(), autoincrement=False, nullable=True))
        batch_op.alter_column('pret_vanzare',
               existing_type=sa.NUMERIC(precision=10, scale=2),
               nullable=False)
        batch_op.alter_column('pret_achizitie',
               existing_type=sa.NUMERIC(precision=10, scale=2),
               nullable=False)
        batch_op.drop_column('pret')

    with op.batch_alter_table('miscari_stoc', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_column('comanda_id')

    with op.batch_alter_table('furnizori', schema=None) as batch_op:
        batch_op.add_column(sa.Column('oras', sa.VARCHAR(length=100), autoincrement=False, nullable=True))
        batch_op.add_column(sa.Column('email', sa.VARCHAR(length=100), autoincrement=False, nullable=True))
        batch_op.add_column(sa.Column('judet', sa.VARCHAR(length=100), autoincrement=False, nullable=True))
        batch_op.drop_column('sold_furnizor')
        batch_op.drop_column('cont_bancar')
        batch_op.drop_column('cod_fiscal')

    with op.batch_alter_table('facturi', schema=None) as batch_op:
        batch_op.add_column(sa.Column('serie', sa.VARCHAR(length=10), autoincrement=False, nullable=False))
        batch_op.add_column(sa.Column('numar', sa.INTEGER(), autoincrement=False, nullable=False))
        batch_op.add_column(sa.Column('valoare_totala', sa.NUMERIC(precision=10, scale=2), autoincrement=False, nullable=False))
        batch_op.add_column(sa.Column('metoda_plata', sa.VARCHAR(length=50), autoincrement=False, nullable=True))
        batch_op.add_column(sa.Column('achitata', sa.BOOLEAN(), autoincrement=False, nullable=True))
        batch_op.add_column(sa.Column('data_emitere', sa.DATE(), autoincrement=False, nullable=False))
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_constraint('uix_serie_numar', type_='unique')
        batch_op.create_unique_constraint('uix_serie_numar', ['serie', 'numar'])
        batch_op.alter_column('client_id',
               existing_type=sa.INTEGER(),
               nullable=False)
        batch_op.alter_column('valoare_tva',
               existing_type=sa.NUMERIC(precision=10, scale=2),
               nullable=False)
        batch_op.drop_column('furnizor_id')
        batch_op.drop_column('modalitate_plata')
        batch_op.drop_column('valoare')
        batch_op.drop_column('nr_factura')
        batch_op.drop_column('serie_factura')
        batch_op.drop_column('data_factura')

    # ### end Alembic commands ###
