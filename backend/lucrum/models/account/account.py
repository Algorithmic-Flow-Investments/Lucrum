from datetime import datetime
from typing import Dict

from sqlalchemy import func, select
from sqlalchemy.ext.hybrid import hybrid_property

from lucrum.database import db
from ..base import BaseModel
from ..target import Target
from ..transaction import Transaction
from ...utils import date_range
from .account_balance import AccountBalance
from .account_connection import AccountConnection, ConnectionType


class Account(BaseModel):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(80), nullable=False)
	description = db.Column(db.Text, nullable=True)

	target = db.relationship("Target", uselist=False)

	def __init__(self, name, description=None):
		self.name = name
		self.description = description

		target = Target(self.name, self)
		self.target = target
		db.session.add(target)

	def __repr__(self):
		return '<Account "' + self.name + '">'

	def data_basic(self) -> Dict[str, str]:
		return {'name': self.name, 'balance': self.balance, 'id': self.id, 'description': self.description}

	def add_balance(self, balance, date=None):
		if date is None:
			date = datetime.now()
		b = AccountBalance(date, balance, self)
		db.session.add(b)
		return b

	# Balance
	@hybrid_property
	def balance(self):
		latest_balance = AccountBalance.query.filter(AccountBalance.account_id == self.id).order_by(
			AccountBalance.date.desc()).first()
		if latest_balance is None:
			return 0
		return latest_balance.balance

	# noinspection PyMethodParameters
	@balance.expression
	def balance(cls):
		return select([AccountBalance.balance]).where(cls.id == AccountBalance.account_id).order_by(
			AccountBalance.date.desc()).limit(1).as_scalar()

	def add_transaction(self, amount: float, date: datetime, info: str):
		transaction = Transaction(self, amount, date, info)
		db.session.add(transaction)
		return transaction

	def add_connection(self, update_type: ConnectionType, bank, identifier):
		connection = AccountConnection(self, update_type, bank, identifier)
		db.session.add(connection)
		return connection

	def data_extra(self):
		return dict(
			self.data_basic(),
			**{
				# 'balance_graph': self.balance_graph(),
				'calculated_balance': self.calculated_total()
			})

	def balance_graph(self):
		graph = {
			date.strftime("%Y-%m-%d"): self.calculated_total(date)
			for date in date_range(self.start, datetime.today(), 7)
		}
		graph[self.start.strftime("%Y-%m-%d")] = 0
		return graph

	def update(self, data: Dict) -> None:
		# print(f"== Updating {self} ==")
		self.balance = data['balance']
		for transaction in data['transactions']:
			transaction['info'] = transaction['info'].replace('&amp;', '&')
			if Transaction.query.filter(Transaction.info == transaction['info'], Transaction.account_id == self.id,
										Transaction.amount == transaction['amount'],
										Transaction.date == transaction['date']).first() is None:
				t = Transaction(self, transaction['amount'], transaction['date'], info=transaction['info'])
				# print("Added {}".format(t))
				db.session.add(t)
			else:
				pass
		for transaction in self.transactions:
			transaction.process_internal()
		db.session.commit()  # TODO: No commit in model

	def inferred_balance(self, date=None):
		if date is None:
			date = datetime.now()
		if len(self.balances) == 0:
			# noinspection PyTypeChecker
			total = db.session.query(func.sum(Transaction.amount)).select_from(Transaction).filter(
				Transaction.target_id == self.target.id, Transaction.date <= date).scalar()
			if total is None:
				total = 0
			else:
				total *= -1
			return round(total, 3)
		prv: AccountBalance = AccountBalance.query.filter(AccountBalance.account_id == self.id,
															AccountBalance.date <= date).order_by(
																AccountBalance.date.desc()).first()

		if prv is not None:
			prev_total = db.session.query(func.sum(Transaction.amount)).select_from(Transaction).filter(
				Transaction.target_id == self.target.id, Transaction.date <= date,
				Transaction.date >= prv.date).scalar()
			if prev_total is None:
				prev_total = 0
			prev_total = prv.balance - prev_total
		else:
			prev_total = None

		nxt: AccountBalance = AccountBalance.query.filter(AccountBalance.account_id == self.id,
															AccountBalance.date >= date).order_by(
																AccountBalance.date.asc()).first()
		if nxt is not None:
			next_total = db.session.query(func.sum(Transaction.amount)).select_from(Transaction).filter(
				Transaction.target_id == self.target.id, Transaction.date >= date,
				Transaction.date <= nxt.date).scalar()
			if next_total is None:
				next_total = 0
			next_total = nxt.balance + next_total
		else:
			next_total = prev_total

		if prev_total is None:
			prev_total = next_total

		if next_total is None:
			print("NEXT WAS NULL")
			return 0

		if next_total != prev_total:
			print("PREV AND NEXT ARE OUT OF SYNC!", prev_total, next_total)
			next_total = (prev_total + next_total) / 2

		return next_total

	def calculated_total(self, date=None):
		if date is None:
			date = datetime.today()
		if self.bankLink is not None:
			# noinspection PyTypeChecker
			total = Transaction.query.with_entities(func.sum(Transaction.amount)).filter(
				Transaction.account_id == self.id, Transaction.date >= date).scalar()
			if total is None:
				total = 0
			return round(self.balance - total, 3)
		else:
			# noinspection PyTypeChecker
			total = Transaction.query.with_entities(func.sum(Transaction.amount)).filter(
				Transaction.target_id == self.target.id, Transaction.date <= date).scalar()
			if total is None:
				total = 0
			else:
				total *= -1
			return round(total, 3)

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