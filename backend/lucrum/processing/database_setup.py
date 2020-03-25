import os

from dateutil.parser import parse

from ..app_basic import basic_app
from ..database import db
# noinspection PyUnresolvedReferences
from ..models import *
from json import load

CONFIG_FILE = os.path.join(os.getcwd(), 'private_config.json')
with open(CONFIG_FILE, 'r') as f:
	CONFIG = load(f)


def setup():
	with basic_app().app_context():
		print("Setup: Start")
		db.reflect()
		if len(db.engine.table_names()) == 0:
			create_database()

		account_connection_users_setup()
		account_setup()
		budgets_setup()


def create_database():
	print("Setup: Create schema")
	db.create_all()
	db.session.commit()


def account_connection_users_setup():
	print("Setup: Account connection users")
	for account_connection_user in CONFIG['account_connection_users']:
		acu: AccountConnectionUser = AccountConnectionUser.query.filter(
			AccountConnectionUser.bank == account_connection_user['bank'],
			AccountConnectionUser.connection_type == account_connection_user['connection_type']).first()
		if acu is None:
			acu = AccountConnectionUser(account_connection_user['connection_type'], account_connection_user['bank'],
										account_connection_user['token'])
			db.session.add(acu)
		else:
			acu.set_token(account_connection_user['token'])
	db.session.commit()


def account_setup():
	print("Setup: Accounts")
	for account in CONFIG['accounts']:
		acc: Account = Account.query.filter(Account.name == account['name']).first()
		if acc is None:
			acc = Account(account['name'], account['description'])
			db.session.add(acc)
		else:
			acc.description = account['description']
		for connection in account['connections']:
			con: AccountConnection = AccountConnection.query.filter(
				AccountConnection.connection_type == connection['connection_type'],
				AccountConnection.bank == connection['bank'], AccountConnection.account_id == acc.id).first()
			if con is None:
				acc.add_connection(connection['connection_type'], connection['bank'], connection['identifier'],
									connection['balance_enabled'], connection['transactions_enabled'])
			else:
				con.balance_enabled = connection['balance_enabled']
				con.transactions_enabled = connection['transactions_enabled']
				con.identifier = connection['identifier']
	db.session.commit()


def budgets_setup():
	print("Setup: budgets")
	overall = Budget.query.filter(Budget.name == 'Overall').first()
	if overall is None:
		overall = Budget('Overall')
		db.session.add(overall)
	overall.categories = [category for category in Category.query.all()]
	db.session.commit()

	for budget in CONFIG['budgets']:
		bdg: Budget = Budget.query.filter(Budget.name == budget['name']).first()
		total = budget['total']
		period = Budget.Period[budget['period'].upper()]
		start = parse(budget['start'])
		end = parse(budget['end']) if budget['end'] is not "" else None
		if bdg is None:
			bdg = Budget(budget['name'], total, start, end, period)
			db.session.add(bdg)
		else:
			bdg.total = total
			bdg.period = period
			bdg.startDate = start
			bdg.endDate = end
		for c in budget['categories']:
			category = Category.query.filter(Category.name == c).first()
			if category is not None:
				bdg.categories.append(category)
	db.session.commit()
