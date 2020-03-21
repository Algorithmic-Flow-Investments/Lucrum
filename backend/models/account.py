from datetime import datetime
from typing import Dict

from sqlalchemy import func

from database import db
from models.base import BaseModel
from models.target import Target
from models.transaction import Transaction
from utils import date_range


class Account(BaseModel):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(80), nullable=False)
	balance = db.Column(db.Float, nullable=False)
	max = db.Column(db.Float, nullable=True)
	min = db.Column(db.Float, nullable=True)
	identifier = db.Column(db.String(80), nullable=True)
	description = db.Column(db.Text, nullable=True)

	bankLink_id = db.Column(db.Integer, db.ForeignKey('bank_link.id'), nullable=True)
	bankLink = db.relationship('BankLink', backref=db.backref('accounts', lazy=True), foreign_keys=[bankLink_id])

	target = db.relationship("Target", uselist=False)

	def __init__(self, name, identifier=None, description=None, balance=0):
		self.name = name
		self.identifier = identifier
		self.description = description
		self.balance = balance

		target = Target(self.name, self)
		self.target = target
		db.session.add(target)

	def __repr__(self):
		return '<Account "' + self.name + '">'

	def data_basic(self) -> Dict[str, str]:
		return {'name': self.name, 'amount': self.balance, 'id': self.id, 'description': self.description}

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
