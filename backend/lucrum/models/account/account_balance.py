from ..base import BaseModel
from ...database import db


class AccountBalance(BaseModel):
	id = db.Column(db.Integer, primary_key=True)

	account_id = db.Column(db.Integer, db.ForeignKey('account.id'), nullable=False)
	account = db.relationship('Account', backref=db.backref('balances', lazy=True), foreign_keys=[account_id])

	balance = db.Column(db.Float)
	date = db.Column(db.DateTime)

	def __init__(self, date, balance, account):
		self.date = date
		self.balance = balance
		self.account = account
