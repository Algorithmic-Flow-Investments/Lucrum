from datetime import datetime
from typing import List, Optional, TYPE_CHECKING

from lucrum.banking2.scrape import new_scraper
from ..transaction import Transaction, TransactionImported
from ..base import BaseModel
from ...database import db
from enum import Enum
from pickle import dumps, loads
try:
	from ...banking2.plaid import plaid_api
except ImportError:
	print("This should only be thrown during testing")

if TYPE_CHECKING:
	from ..transaction import Transaction
	from .account import Account


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

	balance_enabled = db.Column(db.Boolean)
	transactions_enabled = db.Column(db.Boolean)

	def __init__(self,
					account: "Account",
					update_type: ConnectionType,
					bank: str,
					identifier: str,
					balance_enabled: bool = True,
					transactions_enabled: bool = True):
		self.account = account
		self.connection_type = update_type
		self.bank = bank
		self.identifier = identifier
		self.user = AccountConnectionUser.query.filter(
			AccountConnectionUser.bank == self.bank,
			AccountConnectionUser.connection_type == self.connection_type).first()

		self.balance_enabled = balance_enabled
		self.transactions_enabled = transactions_enabled

	def update_balance(self, balance: float) -> float:
		return self.account.add_balance(balance, datetime.now()).balance

	def add_transaction(self, amount, date, info, import_datetime) -> Optional[Transaction]:
		return self.account.add_transaction(amount, date, info, import_datetime)

	def add_balance(self, balance):
		return self.account.add_balance(balance, datetime.now())


class AccountConnectionUser(BaseModel):
	id = db.Column(db.Integer, primary_key=True)

	# TODO: Replace key with composite key
	token = db.Column(db.String)
	bank = db.Column(db.String)
	connection_type = db.Column(db.Enum(ConnectionType))

	def __init__(self, connection_type, bank, token):
		self.set_token(token)
		self.connection_type = connection_type
		self.bank = bank

	def set_token(self, token):
		if type(token) == dict:
			token = dumps(token, 0).decode()
		self.token = token

	def update_balances(self):
		if not any([con.balance_enabled for con in self.connections]):
			return
		if self.connection_type == ConnectionType.PLAID:
			all_balances = plaid_api.get_balance(self.token)
			connection: AccountConnection
			for connection in self.connections:
				account = next((b for b in all_balances if b['account_id'] == connection.identifier), None)
				if account is not None:
					connection.update_balance(account['balances']['current'])
		if self.connection_type == ConnectionType.SCRAPE:
			token = loads(self.token.encode())
			scraper = new_scraper(self.bank, token)
			scraper.login()
			con: AccountConnection
			for con in self.connections:
				balance = scraper.get_balance(con.identifier)
				con.add_balance(balance)
			scraper.quit()

	def update_transactions(self,
							start_date: datetime = None,
							end_date: datetime = None,
							latest=False) -> List[Transaction]:
		if not any([con.transactions_enabled for con in self.connections]):
			return []

		if start_date is None:
			start_date = datetime(1970, 1, 1)
		if end_date is None:
			end_date = datetime.now()

		new_transactions: List[Transaction] = []
		import_datetime = datetime.now()
		if self.connection_type == ConnectionType.PLAID:
			if latest:
				start_date = min([
					t.data_imported.date if t is not None else start_date for t in [
						Transaction.query.filter(
							Transaction.account_id == connection.account_id).order_by(Transaction.date.desc()).first()
						for connection in self.connections
					]
				],
									default=datetime(1970, 1, 1))
			all_transactions = plaid_api.get_transactions(self.token, start_date, end_date)
			for transaction in all_transactions:
				connection: AccountConnection
				for connection in self.connections:
					if transaction['account_id'] == connection.identifier:
						date = datetime.strptime(transaction['date'], "%Y-%m-%d")
						if transaction['authorized_date'] is not None:
							auth_date = datetime.strptime(transaction['authorized_date'], "%Y-%m-%d")
							if auth_date < date:
								date = auth_date
						t = connection.add_transaction(-transaction['amount'], date, transaction['name'],
														import_datetime)
						if t is not None:
							new_transactions.append(t)
							print("Add", t, transaction)
						else:
							print("Duplicate", transaction)

		if self.connection_type == ConnectionType.SCRAPE:
			token = loads(self.token.encode())
			scraper = new_scraper(self.bank, token)
			scraper.login()
			con: AccountConnection
			for con in self.connections:
				if latest:
					lt = Transaction.query.join(TransactionImported).filter(
						Transaction.account_id == con.account_id).order_by(TransactionImported.date.desc()).first()
					if lt is not None:
						start_date = lt.data_imported.date
				for transaction in scraper.get_transactions(con.identifier, start_date, end_date):
					t = con.add_transaction(transaction['amount'], transaction['date'], transaction['info'],
											import_datetime)
					if t is not None:
						new_transactions.append(t)
						print("Add", t, transaction)
					else:
						print("Duplicate", transaction)
			scraper.quit()
		return new_transactions
