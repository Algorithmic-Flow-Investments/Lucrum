"""Split transaction data between 3 tables

Revision ID: a8cb774be1a5
Revises: 
Create Date: 2020-02-16 21:53:33.428780

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'a8cb774be1a5'
down_revision = None
branch_labels = None
depends_on = None

transaction_helper = sa.Table(
	'transactions',
	sa.MetaData(),
	sa.Column('id', sa.Integer, primary_key=True),
	sa.Column('target_id', sa.Integer()),
	sa.Column('method_id', sa.Integer()),
	sa.Column('manual_target', sa.Boolean()),
	sa.Column('info', sa.Text()),
	sa.Column('amount', sa.Float()),
	sa.Column('date', sa.DateTime()),
)


def upgrade():
	# ### commands auto generated by Alembic - please adjust! ###
	op.create_table('transaction_imported', sa.Column('id', sa.Integer(), nullable=False),
					sa.Column('amount', sa.Float(), nullable=False), sa.Column('date', sa.DateTime(), nullable=False),
					sa.Column('info', sa.Text(), nullable=True), sa.ForeignKeyConstraint(
						['id'],
						['transaction.id'],
					), sa.PrimaryKeyConstraint('id'))
	op.create_table('transaction_inferred', sa.Column('id', sa.Integer(), nullable=False),
					sa.Column('date', sa.DateTime(), nullable=True), sa.Column('reference', sa.Text(), nullable=True),
					sa.Column('target_id', sa.Integer(), nullable=True),
					sa.Column('method_id', sa.Integer(), nullable=True),
					sa.ForeignKeyConstraint(
						['id'],
						['transaction.id'],
					), sa.ForeignKeyConstraint(
						['method_id'],
						['method.id'],
					), sa.ForeignKeyConstraint(['target_id'], ['target.id'], ondelete='SET NULL'),
					sa.PrimaryKeyConstraint('id'))
	op.create_table('transaction_manual', sa.Column('id', sa.Integer(), nullable=False),
					sa.Column('date', sa.DateTime(), nullable=True), sa.Column('reference', sa.Text(), nullable=True),
					sa.Column('amount', sa.Float(), nullable=True), sa.Column('target_id', sa.Integer(), nullable=True),
					sa.Column('method_id', sa.Integer(), nullable=True),
					sa.ForeignKeyConstraint(
						['id'],
						['transaction.id'],
					), sa.ForeignKeyConstraint(['method_id'], ['method.id'], ondelete='SET NULL'),
					sa.ForeignKeyConstraint(['target_id'], ['target.id'], ondelete='SET NULL'),
					sa.PrimaryKeyConstraint('id'))
	op.drop_table('transaction_data_manual')
	op.drop_table('tag_string')
	op.drop_table('tag_targets')
	op.drop_table('transaction_data_auto')
	op.drop_constraint(None, 'transaction', type_='foreignkey')
	op.drop_constraint(None, 'transaction', type_='foreignkey')
	op.drop_constraint(None, 'transaction', type_='foreignkey')
	op.drop_column('transaction', 'parent_transaction_id')
	op.drop_column('transaction', 'method_id')
	op.drop_column('transaction', 'manual_method')
	op.drop_column('transaction', 'manual_target')
	op.drop_column('transaction', 'target_id')
	op.drop_constraint(None, 'transaction_tags', type_='foreignkey')
	op.create_foreign_key(None, 'transaction_tags', 'transaction_manual', ['transaction_id'], ['id'])
	# ### end Alembic commands ###


def downgrade():
	# ### commands auto generated by Alembic - please adjust! ###
	op.drop_constraint(None, 'transaction_tags', type_='foreignkey')
	op.create_foreign_key(None, 'transaction_tags', 'transaction', ['transaction_id'], ['id'])
	op.add_column('transaction', sa.Column('target_id', sa.INTEGER(), nullable=True))
	op.add_column('transaction', sa.Column('manual_target', sa.BOOLEAN(), nullable=True))
	op.add_column('transaction', sa.Column('manual_method', sa.BOOLEAN(), nullable=True))
	op.add_column('transaction', sa.Column('method_id', sa.INTEGER(), nullable=True))
	op.add_column('transaction', sa.Column('parent_transaction_id', sa.INTEGER(), nullable=True))
	op.create_foreign_key(None, 'transaction', 'target', ['target_id'], ['id'], ondelete='SET NULL')
	op.create_foreign_key(None, 'transaction', 'transaction', ['parent_transaction_id'], ['id'])
	op.create_foreign_key(None, 'transaction', 'method', ['method_id'], ['id'])
	op.create_table('transaction_data_auto', sa.Column('id', sa.INTEGER(), nullable=False),
					sa.Column('amount', sa.FLOAT(), nullable=False), sa.Column('date', sa.DATETIME(), nullable=False),
					sa.Column('info', sa.TEXT(), nullable=True), sa.Column('reference', sa.TEXT(), nullable=True),
					sa.ForeignKeyConstraint(
						['id'],
						['transaction.id'],
					), sa.PrimaryKeyConstraint('id'))
	op.create_table('tag_targets', sa.Column('tag_id', sa.INTEGER(), nullable=True),
					sa.Column('target_id', sa.INTEGER(), nullable=True),
					sa.ForeignKeyConstraint(
						['tag_id'],
						['tag.id'],
					), sa.ForeignKeyConstraint(
						['target_id'],
						['target.id'],
					))
	op.create_table('tag_string', sa.Column('id', sa.INTEGER(), nullable=False),
					sa.Column('string', sa.TEXT(), nullable=False), sa.Column('parent_id', sa.INTEGER(), nullable=True),
					sa.ForeignKeyConstraint(['parent_id'], ['tag.id'], ondelete='CASCADE'),
					sa.PrimaryKeyConstraint('id'))
	op.create_table('transaction_data_manual', sa.Column('id', sa.INTEGER(), nullable=False),
					sa.Column('amount', sa.FLOAT(), nullable=True), sa.Column('date', sa.DATETIME(), nullable=True),
					sa.ForeignKeyConstraint(
						['id'],
						['transaction.id'],
					), sa.PrimaryKeyConstraint('id'))
	op.drop_table('transaction_manual')
	op.drop_table('transaction_inferred')
	op.drop_table('transaction_imported')
	# ### end Alembic commands ###
