from datetime import datetime
from functools import reduce
from typing import Dict, Optional

from sqlalchemy import func, select
from sqlalchemy.ext.hybrid import hybrid_property

from lucrum.database import db
from ..base import BaseModel
from ..target import Target
from ..transaction import Transaction, TransactionImported
from ...utils import date_range, Interval
from .account_balance import AccountBalance
from .account_connection import AccountConnection, ConnectionType


class Account(BaseModel):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(80), nullable=False)
	description = db.Column(db.Text, nullable=True)

	target_id = db.Column(db.Integer, db.ForeignKey('target.id'), nullable=False)
	target = db.relationship(
		'Target',
		foreign_keys=[target_id],
		back_populates="internal_account",
		cascade="all, delete",
	)

	def __init__(self, name, description=None):
		self.name = name
		self.description = description

		target = Target(self.name)
		self.target = target
		db.session.add(target)

	def __repr__(self):
		return '<Account "' + self.name + '">'

	def data_basic(self) -> Dict[str, str]:
		return {'name': self.name, 'balance': self.balance, 'id': self.id, 'description': self.description}

	def data_extra(self):
		return dict(
			self.data_basic(),
			**{
				# 'balance_graph': self.balance_graph(),
			})

	def add_balance(self, balance, date=None):
		if date is None:
			date = datetime.now()
		b = AccountBalance(date, balance, self)
		db.session.add(b)
		return b

	# Balance
	@hybrid_property
	def balance(self):
		# latest_balance = AccountBalance.query.filter(AccountBalance.account_id == self.id).order_by(
		# 	AccountBalance.date.desc()).first()
		# if latest_balance is None:
		# 	return 0
		# return latest_balance.balance
		return self.inferred_balance()

	# noinspection PyMethodParameters
	@balance.expression
	def balance(cls):
		return select([AccountBalance.balance]).where(cls.id == AccountBalance.account_id).order_by(
			AccountBalance.date.desc()).limit(1).as_scalar()

	def add_transaction(self,
						amount: float,
						date: datetime,
						info: str,
						import_date: datetime = None) -> Optional[Transaction]:
		if TransactionImported.query.join(Transaction).filter(
			Transaction.id == TransactionImported.id, Transaction.account_id == self.id,
			TransactionImported.info == info, TransactionImported.amount == amount, TransactionImported.date == date,
			TransactionImported.import_date != import_date).first() is None:
			info = info.replace("&amp;", "&")
			transaction = Transaction(self, amount, date, info, import_date)
			db.session.add(transaction)
			return transaction
		else:
			return None

	def add_connection(self,
						connection_type: ConnectionType,
						bank,
						identifier,
						balance_enabled=True,
						transactions_enabled=True):
		connection = AccountConnection(self, connection_type, bank, identifier, balance_enabled, transactions_enabled)
		db.session.add(connection)
		return connection

	def balance_graph(self, min_date: datetime, max_date: datetime, interval: Interval = Interval.MONTH):
		if min_date < self.start:
			min_date = self.start
		if max_date > datetime.now():
			max_date = datetime.now()
		graph = {
			date.strftime("%Y-%m-%d"): self.inferred_balance(date)
			for date in date_range(min_date, max_date, interval, snap_end=True)
		}
		graph[self.start.strftime("%Y-%m-%d")] = 0
		return graph

	def inferred_balance(self, date=None):
		if date is None:
			date = datetime.now()
		# print("==", date, "==", self, "==")

		def _inferred_balance_from_prev():

			prev_balance: AccountBalance = AccountBalance.query.filter(AccountBalance.account_id == self.id,
																		AccountBalance.date <= date).order_by(
																			AccountBalance.date.desc()).first()

			if prev_balance is None:
				prev_balance = AccountBalance(datetime.min, 0, self)

			account_transactions_sum_since_prev = db.session.query(func.sum(
				Transaction.amount)).select_from(Transaction).filter(Transaction.account_id == self.id,
																		Transaction.date <= date,
																		Transaction.date >= prev_balance.date).scalar()
			if account_transactions_sum_since_prev is None:
				account_transactions_sum_since_prev = 0

			target_transaction_since_prev = Transaction.query.filter(Transaction.target_id == self.target_id,
																		Transaction.date <= date,
																		Transaction.date >= prev_balance.date).all()
			target_transaction_sum_since_prev = reduce(
				lambda a, b: a + b.amount,
				filter(lambda t: t.mirrored_transaction is None, target_transaction_since_prev), 0)

			inferred_prev_balance = prev_balance.balance + account_transactions_sum_since_prev - target_transaction_sum_since_prev

			# print("PREV", inferred_prev_balance, prev_balance, account_transactions_sum_since_prev,
			# 		target_transaction_sum_since_prev)
			return inferred_prev_balance

		def _inferred_balance_from_next():
			next_balance: AccountBalance = AccountBalance.query.filter(AccountBalance.account_id == self.id,
																		AccountBalance.date >= date).order_by(
																			AccountBalance.date.asc()).first()
			if next_balance is None:
				# print("No next balance")
				return None

			account_transactions_sum_before_next = db.session.query(func.sum(
				Transaction.amount)).select_from(Transaction).filter(Transaction.account_id == self.id,
																		Transaction.date > date,
																		Transaction.date <= next_balance.date).scalar()
			# print(
			# 	"transaction_before_next",
			# 	Transaction.query.filter(Transaction.account_id == self.id, Transaction.date > date,
			# 								Transaction.date <= next_balance.date).all())
			if account_transactions_sum_before_next is None:
				account_transactions_sum_before_next = 0

			target_transaction_before_next = Transaction.query.filter(Transaction.target_id == self.target_id,
																		Transaction.date >= date,
																		Transaction.date <= next_balance.date).all()

			# for t in filter(lambda t: t.mirrored_transaction is None, target_transaction_before_next):
			# 	print("ttbn", t, t.mirrored_transaction, t.data_imported.date)

			# print(">>?", Transaction.query.filter(Transaction.amount == 1000, Transaction.account_id == 1).first())

			target_transaction_sum_before_next = reduce(
				lambda a, b: a + b.amount,
				filter(lambda t: t.mirrored_transaction is None, target_transaction_before_next), 0)

			inferred_next_balance = next_balance.balance - account_transactions_sum_before_next + target_transaction_sum_before_next

			# print(
			# 	"account transactions\n\t\t", "\n\t\t".join(
			# 		str(t) for t in Transaction.query.filter(Transaction.account_id == self.id, Transaction.date > date,
			# 													Transaction.date <= next_balance.date).order_by(
			# 														Transaction.date.desc()).all()))

			# print("NEXT", inferred_next_balance, next_balance, account_transactions_sum_before_next,
			# 		target_transaction_sum_before_next)
			return inferred_next_balance

		inb = _inferred_balance_from_next()
		if inb is None:
			return _inferred_balance_from_prev()
		return inb

	@property
	def start(self):
		first = Transaction.query.filter(Transaction.account_id == self.id).order_by(Transaction.date.asc()).first()
		if first is None:
			first = Transaction.query.filter(Transaction.target_id == self.target.id).order_by(
				Transaction.date.asc()).first()
		if first is None:
			return datetime.today()
		return first.date

	@property
	def end(self):
		first = Transaction.query.filter(Transaction.account_id == self.id).order_by(Transaction.date.desc()).first()
		if first is None:
			first = Transaction.query.filter(Transaction.target_id == self.target.id).order_by(
				Transaction.date.desc()).first()

		return first.date
