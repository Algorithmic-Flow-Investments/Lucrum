from datetime import datetime, timedelta
from typing import Optional

from sqlalchemy import select, text, or_, and_
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.sql.functions import coalesce

from ...database import db
from ..base import BaseModel
from ..method import Method
from ..target import Target
from .transaction_imported import TransactionImported
from .transaction_inferred import TransactionInferred
from .transaction_manual import TransactionManual


class Transaction(BaseModel):
	id = db.Column(db.Integer, primary_key=True)

	account_id = db.Column(db.Integer, db.ForeignKey('account.id'), nullable=False)
	account = db.relationship('Account', backref=db.backref('transactions', lazy=True), foreign_keys=[account_id])

	data_imported = db.relationship(TransactionImported, backref="parent", cascade="all, delete", uselist=False)
	data_inferred = db.relationship(TransactionInferred, backref="parent", cascade="all, delete", uselist=False)
	data_manual = db.relationship(TransactionManual, backref="parent", cascade="all, delete", uselist=False)

	tags = db.relationship(
		"Tag",
		secondary="outerjoin(Tag, target_tags, target_tags.c.tag_id == Tag.id)."
		"outerjoin(transaction_tags, transaction_tags.c.tag_id == Tag.id)",
		primaryjoin=
		"or_(Transaction.target_id == target_tags.c.target_id, Transaction.id == transaction_tags.c.transaction_id)",
		secondaryjoin="or_(Tag.id == transaction_tags.c.tag_id, Tag.id == target_tags.c.tag_id)",
		backref="transactions",
		uselist=True,
		viewonly=True)

	scheduled_id = None

	# parent_transaction_id = db.Column(db.Integer, db.ForeignKey('transaction.id'))
	# linked_transactions = db.relationship('Transaction', backref=db.backref('parent_transaction', remote_side=[id]))

	def __init__(self, account, amount: float, date: datetime, info=None, import_date=None):
		if import_date is None:
			import_date = datetime.now()
		self.account = account

		self.data_imported = TransactionImported(self, amount, date, info, import_date)
		self.data_inferred = TransactionInferred(self)
		self.data_manual = TransactionManual(self)

	# Info
	@hybrid_property
	def info(self):
		return self.data_imported.info

	# noinspection PyMethodParameters
	@info.expression
	def info(cls):
		return select([TransactionImported.info]).where(cls.id == TransactionImported.id).as_scalar()

	# Amount
	@hybrid_property
	def amount(self):
		return self.data_manual.amount or self.data_imported.amount

	# noinspection PyMethodParameters
	@amount.expression
	def amount(cls):
		return Transaction.construct_coalesce(cls, manual=TransactionManual.amount, imported=TransactionImported.amount)

	def set_amount(self, value):
		self.data_manual.amount = value

	# Date
	@hybrid_property
	def date(self) -> datetime:
		return self.data_manual.date or self.data_inferred.date or self.data_imported.date

	# noinspection PyMethodParameters,PyMethodParameters,PyMethodParameters
	@date.expression
	def date(cls):
		return Transaction.construct_coalesce(cls,
												manual=TransactionManual.date,
												inferred=TransactionInferred.date,
												imported=TransactionImported.date)

	def set_date(self, value):
		self.data_manual.date = value

	# Target
	@hybrid_property
	def target_id(self):
		return self.data_manual.target_id or self.data_inferred.target_id

	# noinspection PyMethodParameters
	@target_id.expression
	def target_id(cls):
		return Transaction.construct_coalesce(cls,
												manual=TransactionManual.target_id,
												inferred=TransactionInferred.target_id)

	@property
	def target(self):
		return Target.query.filter(Target.id == self.target_id).first()

	def set_target(self, value):
		if type(value) == Target:
			value = value.id
		self.data_manual.target_id = value

	# Method
	@hybrid_property
	def method_id(self):
		return self.data_manual.method_id or self.data_inferred.method_id

	# noinspection PyMethodParameters
	@method_id.expression
	def method_id(cls):
		return Transaction.construct_coalesce(cls,
												manual=TransactionManual.method_id,
												inferred=TransactionInferred.method_id)

	@property
	def method(self):
		return Method.query.filter(Method.id == self.method_id).first()

	def set_method(self, value):
		if type(value) == Method:
			value = value.id
		self.data_manual.method_id = value

	# noinspection PyMissingTypeHints
	@staticmethod
	def construct_coalesce(cls, manual=None, inferred=None, imported=None):
		if manual and inferred and imported:
			return coalesce(
				select([manual]).where(cls.id == TransactionManual.id).as_scalar(),
				coalesce(
					select([inferred]).where(cls.id == TransactionInferred.id).as_scalar(),
					select([imported]).where(cls.id == TransactionImported.id).as_scalar()))
		if manual and imported:
			return coalesce(
				select([manual]).where(cls.id == TransactionManual.id).as_scalar(),
				select([imported]).where(cls.id == TransactionImported.id).as_scalar())
		if manual and inferred:
			return coalesce(
				select([manual]).where(cls.id == TransactionManual.id).as_scalar(),
				select([inferred]).where(cls.id == TransactionInferred.id).as_scalar())
		if inferred and imported:
			return coalesce(
				select([inferred]).where(cls.id == TransactionInferred.id).as_scalar(),
				select([imported]).where(cls.id == TransactionImported.id).as_scalar())

	@property
	def alt_amount(self):  # TODO: Re-add linked account, move to inferred?
		return self.amount

	# return round(self.amount - sum(transaction.amount for transaction in self.linked_transactions), 2)

	def process(self):
		from ...processing import process_transactions
		process_transactions.process_transaction(self)

	def __repr__(self):
		return '<Transaction ({}) {} to {} at {} on {} using {} tags: {}>'.format(self.id, self.amount, self.account,
																					self.target, self.date, self.method,
																					self.tags)

	def data_extra(self):
		return dict(
			self.data_basic(), **{
				'amount_extra': {
					'imported': self.data_imported.amount,
					'manual': self.data_manual.amount
				},
				'method_id': self.method_id,
				'method_id_extra': {
					'inferred': self.data_inferred.method_id,
					'manual': self.data_manual.method_id
				},
				'target_id_extra': {
					'inferred': self.data_inferred.target_id,
					'manual': self.data_manual.target_id
				},
				'date_extra': {
					'imported': self.data_imported.date,
					'inferred': self.data_inferred.date,
					'manual': self.data_manual.date
				}
			})

	def data_basic(self):
		return {
			'id': self.id,
			'amount': self.alt_amount,
			'date': self.date,
			'target_id': self.target.id if self.target else None,
			'account_id': self.account.id,
			'tag_ids': [tag.id for tag in self.tags],
			'raw_info': self.info,
			'scheduled_id': self.scheduled_id
		}

	@property
	def mirrored_transaction(self) -> Optional["Transaction"]:
		if (not self.target) or (not self.target.internal_account_id):
			return None

		date_allowance = or_(Transaction.date == self.date, Transaction.date == self.date + timedelta(1),
								Transaction.date == self.date - timedelta(1))
		return Transaction.query.join(Target, Target.id == Transaction.target_id).join(Transaction.account).filter(
			Transaction.amount == -self.amount, date_allowance,
			Transaction.target_id == Target.id, Target.internal_account_id == self.account_id,
			text(f"{self.target.internal_account_id} = account.id")).first()
