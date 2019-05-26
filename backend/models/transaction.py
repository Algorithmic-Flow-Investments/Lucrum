from sqlalchemy.orm import aliased

from database import db
from models import Tag, Method, MethodString, Target, TargetString, target_tags, transaction_tags
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy import case, select, join, or_, and_, func


class Transaction(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	amount = db.Column(db.Float, nullable=False)
	date = db.Column(db.DateTime, nullable=False)
	raw_info = db.Column(db.Text, nullable=True)

	manual_tags = db.relationship('Tag', secondary='transaction_tags')


	account_id = db.Column(db.Integer, db.ForeignKey('account.id'), nullable=True)
	account = db.relationship('Account', backref=db.backref('transactions', lazy=True), foreign_keys=[account_id])

	target_id = db.Column(db.Integer, db.ForeignKey('target.id', ondelete="SET NULL"), nullable=True)
	target = db.relationship('Target', backref=db.backref('transactions'), foreign_keys=[target_id])

	method_id = db.Column(db.Integer, db.ForeignKey('method.id'), nullable=True)
	method = db.relationship('Method', backref=db.backref('transactions', lazy=True), foreign_keys=[method_id])

	# This will have to do for now, I spent literally 6 hours trying to make it work with manual tags
	tags = db.relationship('Tag', secondary='target_tags', primaryjoin="Transaction.target_id==target_tags.c.target_id")

	parent_transaction_id = db.Column(db.Integer, db.ForeignKey('transaction.id'))
	linked_transactions = db.relationship("Transaction",
							backref=db.backref('parent_transaction', remote_side=[id])
							)

	@classmethod
	def __declare_last__(cls):

		j = join(Tag, target_tags, Tag.id==target_tags.c.tag_id, isouter=True) \
			.join(Transaction, target_tags.c.target_id == Transaction.target_id, isouter=True)#join(Tag, transaction_tags, Tag.id==transaction_tags.c.tag_id, isouter=True)\


		print(j)

		"""cls.tags = db.relationship(Tag, secondary=j,
								   primaryjoin="Tag.id==remote(target_tags.c.tag_id)",
								   secondaryjoin="Transaction.target_id==foreign(target_tags.c.target_id)")"""

	def __init__(self, account, amount: float, date, target=None, method=None, info=None):
		self.account = account
		self.raw_info = info
		self.amount = amount
		self.date = date

		if type(target) == str:
			target = Target.query.filter_by(name=target).first()

		if target is not None:
			self.target = target

		if type(method) == str:
			method = Method.query.filter_by(name=method).first()

		if method is not None:
			self.target = method

		self.process()

	def process_type(self, dataString, one=True):
		raw = self.raw_info.lower()
		for datStr in dataString.query.all():
			if raw.find(datStr.string) != -1:
				if one and self in datStr.parent.transactions: return
				datStr.parent.transactions.append(self)
				if one: return

	"""@property
	def tags(self):
		return Tag.query\
			.outerjoin(target_tags, Tag.id==target_tags.c.tag_id)\
			.outerjoin(transaction_tags, Tag.id == transaction_tags.c.tag_id) \
			.outerjoin(Transaction, or_(target_tags.c.target_id == Transaction.target_id, Transaction.id == transaction_tags.c.transaction_id)) \
			.filter(Transaction.id==self.id).all()"""

	@property
	def exclude(self):
		return Tag.query.join(Transaction.tags).filter(Transaction.id==self.id, Tag.exclude==True).count() > 0

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

		"""if self.target and self.target.name == "<internal>":
			mirrored_transaction = Transaction.query.join(Target, (Target.name == "<internal>")).filter(
				Transaction.amount == -self.amount, Transaction.date == self.date).first()
			if mirrored_transaction is not None:
				this_account_target = Target.query.filter_by(name=self.account.name).first()
				other_account_target = Target.query.filter_by(name=mirrored_transaction.account.name).first()
				if this_account_target and other_account_target:
					mirrored_transaction.target = this_account_target
					self.target = other_account_target"""

	def process(self):
		if self.raw_info is not None:
			self.process_type(TargetString)
			self.process_type(MethodString)
			self.process_internal()

	def __repr__(self):
		return "<Transaction {} at {} on {} using {} tags: {}>".format(self.amount, self.target, self.date, self.method,
																	   self.tags)

	def data(self):
		return {'amount': self.alt_amount,
				'real_amount': self.amount,
				'id': self.id,
				'date': self.date,
				'target': self.target.data_advanced() if self.target is not None else None,
				'tags': [tag.data_advanced(self) for tag in self.tags],
				'raw': self.raw_info,
				'method': self.method.data_basic() if self.method is not None else None,
				'account': self.account.data_basic()}