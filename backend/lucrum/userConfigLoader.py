from logging import info

from dateutil.parser import parse

from .database import db
from .models import BankLink, Account, Budget, Category
from .user_config import *


def load_accounts():
	info('Loading accounts...')
	# So people on Github can't see my bank details
	bank_user = BankLink(CREDENTIALS['bank'], CREDENTIALS['userid'], CREDENTIALS['password'], CREDENTIALS['passcode'],
							CREDENTIALS['questions'], CREDENTIALS['encryptionkey'])

	for account in ACCOUNTS['auto']:
		if Account.query.filter_by(name=account[0]).first() is None:
			a = Account(account[0], account[1], account[2])
			print("Added new account", a)
			bank_user.accounts.append(a)
	db.session.add(bank_user)

	for account in ACCOUNTS['static']:
		if Account.query.filter_by(name=account[0]).first() is None:
			a = Account(account[0], description=account[1], balance=account[2])
			print("Added new account", a)
			db.session.add(a)


def load_budgets():
	info('Loading budgets...')
	for budget in BUDGETS:
		period = Budget.Period[budget['period'].upper()]
		start = parse(budget['start'])
		end = parse(budget['end']) if budget['end'] is not None else None

		b = Budget(budget['name'], budget['total'], start, end, period)
		db.session.add(b)

		for c in budget['categories']:
			category = Category.query.filter_by(id=c).first()
			b.categories.append(category)
	db.session.commit()
