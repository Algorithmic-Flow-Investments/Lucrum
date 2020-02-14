import sqlalchemy
from sqlalchemy import join, select
from sqlalchemy.ext.hybrid import hybrid_property

from database import db
from models.method import Method, MethodString
from models.tag import Tag, target_tags, transaction_tags
from models.target import Target, TargetString
from datetime import datetime


class Transaction(db.Model):
	id = db.Column(db.Integer, primary_key=True)

	account_id = db.Column(db.Integer, db.ForeignKey('account.id'), nullable=True)
	account = db.relationship('Account', backref=db.backref('transactions', lazy=True), foreign_keys=[account_id])

	data_auto = db.relationship('TransactionDataAuto', backref="parent", uselist=False)

	data_manual = db.relationship('TransactionDataManual', backref="parent", uselist=False)

	target_id = db.Column(db.Integer, db.ForeignKey('target.id', ondelete='SET NULL'), nullable=True)
	target = db.relationship('Target', backref=db.backref('transactions'), foreign_keys=[target_id])
	manual_target = db.Column(db.Boolean)

	method_id = db.Column(db.Integer, db.ForeignKey('method.id'), nullable=True)
	method = db.relationship('Method', foreign_keys=[method_id])
	manual_method = db.Column(db.Boolean)

	auto_tags = db.relationship('Tag',
								secondary='target_tags',
								primaryjoin='Transaction.target_id==target_tags.c.target_id')
	manual_tags = db.relationship('Tag', secondary='transaction_tags')

	tags = db.relationship(
		"Tag",
		secondary="join(Target, target_tags, target_tags.c.target_id == Target.id)."
		"join(Tag, target_tags.c.tag_id == Tag.id)."
		"outerjoin(transaction_tags, transaction_tags.c.tag_id == Tag.id)",
		primaryjoin="or_(Transaction.target_id == Target.id, Transaction.id == transaction_tags.c.transaction_id)",
		secondaryjoin="Tag.id == target_tags.c.tag_id",
		backref="transactions",
		uselist=True)

	parent_transaction_id = db.Column(db.Integer, db.ForeignKey('transaction.id'))
	linked_transactions = db.relationship('Transaction', backref=db.backref('parent_transaction', remote_side=[id]))

	def __init__(self, account, amount: float, date: datetime, info=None):
		self.account = account

		self.data_auto = TransactionDataAuto(self, amount, date, info)
		self.data_manual = TransactionDataManual(self)

		self.manual_target = False
		self.manual_method = False

		self.process()

	# Info
	@hybrid_property
	def info(self):
		return self.data_auto.info

	@info.expression
	def info(cls):
		return select([TransactionDataAuto.info]).where(cls.id == TransactionDataAuto.id).as_scalar()

	# Amount
	@hybrid_property
	def amount(self):
		return self.data_auto.amount

	@amount.expression
	def amount(cls):
		return select([TransactionDataAuto.amount]).where(cls.id == TransactionDataAuto.id).as_scalar()

	# Date
	@hybrid_property
	def date(self):
		return self.data_auto.date

	@date.expression
	def date(cls):
		return select([TransactionDataAuto.date]).where(cls.id == TransactionDataAuto.id).as_scalar()

	@property
	def exclude(self):
		return False  # Tag.query.join(Transaction.tags).filter(Transaction.id == self.id, Tag.exclude == True).count() > 0

	@property
	def alt_amount(self):
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
		if self.info is not None:
			if not self.manual_method:
				method_change = self.process_method()
			if not self.manual_target:
				target_change = self.process_target()
			self.process_internal()
		return method_change or target_change

	def process_method(self):
		old = self.method_id
		raw = self.info.lower()
		for methodStr in MethodString.query.all():
			if raw.find(methodStr.string) != -1:
				self.method_id = methodStr.parent.id
				return self.method_id != old

		self.method_id = None  # TODO: Manual clas
		return False

	def process_target(self):
		old = self.target_id
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
			self.data_auto.reference = split2[0]

		for targetStr in TargetString.query.all():
			if raw.find(targetStr.string) != -1:
				self.target_id = targetStr.parent.id
				return self.target_id != old

		# If ignoring reference doesn't work, include it
		raw = self.info.lower()
		for targetStr in TargetString.query.all():
			if raw.find(targetStr.string) != -1:
				self.target_id = targetStr.parent.id
				return self.target_id != old

		self.target_id = None  # TODO: Manual clas
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


class TransactionDataAuto(db.Model):
	id = db.Column(db.Integer, db.ForeignKey(Transaction.id), primary_key=True)
	amount = db.Column(db.Float, nullable=False)
	date = db.Column(db.DateTime, nullable=False)
	info = db.Column(db.Text, nullable=True)
	reference = db.Column(db.Text, nullable=True)

	def __init__(self, transaction: Transaction, amount: float, date: datetime, info: str):
		self.id = transaction.id
		self.amount = amount
		self.date = date
		self.info = info


class TransactionDataManual(db.Model):
	id = db.Column(db.Integer, db.ForeignKey(Transaction.id), primary_key=True)
	amount = db.Column(db.Float, nullable=True)
	date = db.Column(db.DateTime, nullable=True)

	def __init__(self, transaction):
		self.id = transaction.id
