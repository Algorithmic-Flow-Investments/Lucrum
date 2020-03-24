from datetime import datetime
from logging import info

from ..models import AccountConnectionUser, Transaction
from ..database import db
from .process_transactions import process_transactions_list


def fetch_balances():
	info("Fetching balances")
	usr: AccountConnectionUser
	for usr in AccountConnectionUser.query.all():
		if usr.balance_enabled:
			info(f"Fetching balances for {usr}")
			usr.update_balances()
	db.session.commit()


# TODO: try deleting all transaction and reimporting to see if numbers line up / what is different


def fetch_transactions(latest=True):
	info("Fetching transactions")
	usr: AccountConnectionUser
	new_transactions = []
	for usr in AccountConnectionUser.query.all():
		if usr.transactions_enabled:
			info(f"Fetching transactions for {usr}")
			new_transactions.extend(usr.update_transactions(latest=latest))
	info(f"Added {len(new_transactions)} new transactions")
	info(f"A>: {new_transactions}")
	u = process_transactions_list(new_transactions)
	info(f"updated {u}")
	db.session.commit()
