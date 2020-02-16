import sqlalchemy
from dateutil.parser import parse
from sqlalchemy import join, select, text, ForeignKeyConstraint
from sqlalchemy.sql.functions import coalesce
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import foreign

from database import db
from models.method import Method, MethodString
from models.tag import Tag, target_tags, transaction_tags
from models.target import Target, TargetString
from datetime import datetime
from .transaction_imported import TransactionImported
from .transaction_inferred import TransactionInferred
from .transaction_manual import TransactionManual


class Transaction(db.Model):
	id = db.Column(db.Integer, primary_key=True)

	account_id = db.Column(db.Integer, db.ForeignKey('account.id'), nullable=True)
	account = db.relationship('Account', backref=db.backref('transactions', lazy=True), foreign_keys=[account_id])

	data_imported = db.relationship(TransactionImported, backref="parent", uselist=False)
	data_inferred = db.relationship(TransactionInferred, backref="parent", uselist=False)
	data_manual = db.relationship(TransactionManual, backref="parent", uselist=False)
	tags = db.relationship(
		"Tag",
		secondary="outerjoin(Tag, target_tags, target_tags.c.tag_id == Tag.id)."
		"outerjoin(transaction_tags, transaction_tags.c.tag_id == Tag.id)",
		primaryjoin=
		"or_(Transaction.target_id == target_tags.c.target_id, Transaction.id == transaction_tags.c.transaction_id)",
		secondaryjoin="or_(Tag.id == transaction_tags.c.tag_id, Tag.id == target_tags.c.tag_id)",
		backref="transactions",
		uselist=True)

	#
	# parent_transaction_id = db.Column(db.Integer, db.ForeignKey('transaction.id'))
	# linked_transactions = db.relationship('Transaction', backref=db.backref('parent_transaction', remote_side=[id]))

	def __init__(self, account, amount: float, date: datetime, info=None):
		self.account = account

		self.data_imported = TransactionImported(self, amount, date, info)
		self.data_inferred = TransactionInferred(self)
		self.data_manual = TransactionManual(self)

		self.process()

	# Info
	@hybrid_property
	def info(self):
		return self.data_imported.info

	@info.expression
	def info(cls):
		return select([TransactionImported.info]).where(cls.id == TransactionImported.id).as_scalar()

	# Amount
	@hybrid_property
	def amount(self):
		return self.data_manual.amount or self.data_imported.amount

	@amount.expression
	def amount(cls):
		return Transaction.construct_coalesce(cls, manual=TransactionManual.amount, imported=TransactionImported.amount)

	# Date
	@hybrid_property
	def date(self):
		return self.data_manual.date or self.data_inferred.date or self.data_imported.date

	@date.expression
	def date(cls):
		return Transaction.construct_coalesce(cls,
												manual=TransactionManual.date,
												inferred=TransactionInferred.date,
												imported=TransactionImported.date)

	# Target
	@hybrid_property
	def target_id(self):
		return self.data_manual.target_id or self.data_inferred.target_id

	@target_id.expression
	def target_id(cls):
		return Transaction.construct_coalesce(cls,
												manual=TransactionManual.target_id,
												inferred=TransactionInferred.target_id)

	@property
	def target(self):
		return Target.query.filter(Target.id == self.target_id).first()

	# Method
	@hybrid_property
	def method_id(self):
		return self.data_manual.method_id or self.data_inferred.method_id

	@method_id.expression
	def method_id(cls):
		return Transaction.construct_coalesce(cls,
												manual=TransactionManual.method_id,
												inferred=TransactionInferred.method_id)

	@property
	def method(self):
		return Method.query.filter(Method.id == self.method_id).first()

	# @hybrid_property
	# def tags(self):
	# 	return self.data_manual.tags or self.data_inferred.tags
	#
	# @tags.expression
	# def tags(cls):
	# 	return select([Tag]).where(TransactionManual.tags).where(TransactionManual.id == cls.id)

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
	def alt_amount(self):  # TODO: Integrate this with the actual amount property
		return round(self.amount - sum(transaction.amount for transaction in self.linked_transactions), 2)

	def process_internal(self):
		mirrored_transaction = Transaction.query.filter(Transaction.amount == -self.amount,
														Transaction.date == self.date,
														Transaction.account != self.account).first()
		if mirrored_transaction:
			this_account_target = Target.query.filter_by(name=self.account.name).first()
			other_account_target = Target.query.filter_by(name=mirrored_transaction.account.name).first()
			if this_account_target and other_account_target:
				mirrored_transaction.target = this_account_target
				self.target = other_account_target

	def process(self):
		method_change = False
		target_change = False
		date_change = False
		if self.info is not None:
			method_change = self.process_method()
			target_change = self.process_target()
			date_change = self.process_date()
			# self.process_internal()
		return method_change or target_change or date_change

	def process_date(self):
		old = self.data_inferred.date
		raw = self.info.lower()  # type: str
		if raw.find(' on '):
			split = raw.split(' on ')
			new = parse(split[-1])
			self.data_inferred.date = new
			return old != new
		return False

	def process_method(self):
		old = self.data_inferred.method_id
		raw = self.info.lower()
		for methodStr in MethodString.query.all():
			if raw.find(methodStr.string) != -1:
				self.data_inferred.method_id = methodStr.parent.id
				return self.data_inferred.method_id != old

		self.data_inferred.method_id = None  # TODO: Manual clas
		return False

	def process_target(self):
		old = self.data_inferred.target_id
		raw = self.info.lower()  # type: str
		if raw.find('ref.'):
			split = raw.split('ref.', maxsplit=1)
		elif raw.find('reference') != -1:
			split = raw.split('reference', maxsplit=1)
		if len(split) > 1:
			if split[1].find('from') != -1:
				split2 = split[1].split('from', maxsplit=1)
			else:
				split2 = split[1].split(',', maxsplit=1)
			raw = split[0] + split2[1]
			self.data_inferred.reference = split2[0]

		for targetStr in TargetString.query.all():
			if raw.find(targetStr.string) != -1:
				self.data_inferred.target_id = targetStr.parent.id
				return self.target_id != old

		# If ignoring reference doesn't work, include it
		raw = self.info.lower()
		for targetStr in TargetString.query.all():
			if raw.find(targetStr.string) != -1:
				self.data_inferred.target_id = targetStr.parent.id
				return self.data_inferred.target_id != old

		self.data_inferred.target_id = None  # TODO: Manual clas
		return False

	def __repr__(self):
		return '<Transaction {} at {} on {} using {} tags: {}>'.format(self.amount, self.target, self.date, self.method,
																		self.tags)

	def data_extra(self):
		return dict(self.data_basic(), **{'real_amount': self.amount, 'method_id': self.method_id})

	def data_basic(self):
		return {
			'id': self.id,
			'amount': self.alt_amount,
			'date': self.date,
			'target_id': self.target.id if self.target else None,
			'account_id': self.account.id,
			'tag_ids': [tag.id for tag in self.tags],
			'raw_info': self.info
		}
