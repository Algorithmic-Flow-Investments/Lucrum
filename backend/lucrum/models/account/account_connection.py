from datetime import datetime
from typing import List

from ..base import BaseModel
from ...database import db
from enum import Enum
from ...banking2.plaid import plaid_api


class ConnectionType(Enum):
	PLAID = "PLAID"
	SCRAPE = "SCRAPE"
	API = "API"


class AccountConnection(BaseModel):
	id = db.Column(db.Integer, primary_key=True)

	account_id = db.Column(db.Integer, db.ForeignKey('account.id'), nullable=False)
	account = db.relationship('Account', backref=db.backref('connections', lazy=True), foreign_keys=[account_id])

	connection_type = db.Column(db.Enum(ConnectionType))
	bank = db.Column(db.String)

	user_id = db.Column(db.Integer, db.ForeignKey('account_connection_user.id'), nullable=True)
	user = db.relationship('AccountConnectionUser',
							backref=db.backref('connections', lazy=True),
							foreign_keys=[user_id])

	identifier = db.Column(db.String)

	def __init__(self, account, update_type, bank, identifier):
		self.account = account
		self.connection_type = update_type
		self.bank = bank
		self.identifier = identifier
		self.user = AccountConnectionUser.query.filter(
			AccountConnectionUser.bank == self.bank,
			AccountConnectionUser.connection_type == self.connection_type).first()

	def update_balance(self, balance):
		return self.account.add_balance(balance, datetime.now())

	def add_transaction(self, amount, date, info):
		return self.account.add_transaction(amount, date, info)


class AccountConnectionUser(BaseModel):
	id = db.Column(db.Integer, primary_key=True)

	token = db.Column(db.String)
	bank = db.Column(db.String)
	connection_type = db.Column(db.Enum(ConnectionType))

	def __init__(self, connection_type, bank, token):
		self.token = token
		self.connection_type = connection_type
		self.bank = bank

	def update_balances(self):
		if self.connection_type == ConnectionType.PLAID:
			all_balances = plaid_api.get_balance(self.token)
			print("AB", all_balances)
			connection: AccountConnection
			for connection in self.connections:
				account = next((b for b in all_balances if b['account_id'] == connection.identifier), None)
				print("CON", connection, account)
				if account is not None:
					connection.update_balance(account['balances']['current'])

	def update_transactions(self, start_date: datetime, end_date: datetime):
		new_transactions = []
		if self.connection_type == ConnectionType.PLAID:
			all_transactions = plaid_api.get_transactions(self.token, start_date, end_date)
			for transaction in all_transactions:
				connection: AccountConnection
				for connection in self.connections:
					if transaction['account_id'] == connection.identifier:
						date = datetime.strptime(transaction['date'], "%Y-%m-%d")
						t = connection.add_transaction(-transaction['amount'], date, transaction['name'])
						new_transactions.append(t)
		return new_transactions
