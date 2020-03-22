import enum
from datetime import datetime

from ..database import db
from .base import BaseModel
from . import Account
from .target import Target
from .transaction import Transaction
from ..utils import date_range


class ScheduledTransaction(BaseModel):
	id = db.Column(db.Integer, primary_key=True)

	account_id = db.Column(db.Integer, db.ForeignKey('account.id'), nullable=True)
	account = db.relationship('Account', backref=db.backref('scheduled', lazy=True), foreign_keys=[account_id])

	name = db.Column(db.String(80), nullable=False)
	amount = db.Column(db.Float, nullable=False)
	start_date = db.Column(db.DateTime, nullable=False)

	class Period(enum.Enum):
		WEEK = 1
		MONTH = 2

	period = db.Column(db.Enum(Period), nullable=True)

	end_date = db.Column(db.DateTime, nullable=True)

	target_id = db.Column(db.Integer, db.ForeignKey('target.id'), nullable=True)
	target = db.relationship('Target', backref=db.backref('scheduled', lazy=True), foreign_keys=[target_id])

	tags = db.relationship("Tag",
							secondary="outerjoin(Tag, target_tags, target_tags.c.tag_id == Tag.id)",
							primaryjoin="ScheduledTransaction.target_id==target_tags.c.target_id")

	def __init__(self,
					account: Account,
					name: str,
					amount: int,
					start_date: datetime,
					target: Target,
					period: Period = None,
					end_date: datetime = None):
		self.account = account
		self.name = name
		self.amount = amount
		self.start_date = start_date
		self.end_date = end_date
		self.period = period

		if period is None and end_date is None:
			self.end_date = self.start_date

		self.target_id = target.id

	def data_basic(self):
		return {
			'id': self.id,
			'name': self.name,
			'amount': self.amount,
			'start_date': self.start_date,
			'end_date': self.end_date,
			'period': self.period,
			'target_id': self.target_id
		}

	def occurrence_data(self, date: datetime):
		return {
			'id': self.id,
			'amount': self.amount,
			'date': date,
			'target_id': self.target_id,
			'account_id': self.account.id,
			'tag_ids': [tag.id for tag in self.tags],
			'raw_info': "SCHEDULED"
		}

	def occurred_transaction(self, date: datetime):
		transaction = Transaction(self.account, self.amount, date, "SCHEDULED")
		transaction.data_manual.target = self.target
		transaction.scheduled_id = self.id
		return transaction

	def get_occurrences(self, min_date: datetime, max_date: datetime):
		if self.period is ScheduledTransaction.Period.MONTH:
			for date in date_range(min_date, max_date):
				if date.day == self.start_date.day:
					yield self.occurred_transaction(date)
		elif self.period is ScheduledTransaction.Period.WEEK:
			for date in date_range(min_date, max_date):
				if date.weekday() == self.start_date.weekday():
					yield self.occurred_transaction(date)
		else:
			if min_date <= self.start_date <= max_date:
				yield self.occurred_transaction(self.start_date)
