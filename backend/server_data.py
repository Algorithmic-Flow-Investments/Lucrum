from datetime import datetime, timedelta
from logging import info

import prebuilt
from database import db
from models import BankLink, Transaction
from processing import process_transactions
from userConfigLoader import load_accounts, load_budgets
from user_config import CREDENTIALS


def new_database():
	db.reflect()

	info('Dropping database...')
	db.drop_all()

	info('Creating database...')
	db.create_all()

	load_accounts()

	prebuilt.load_all()

	load_budgets()

	db.session.commit()


def populate_database(force=False, latest=True):
	info('Fetching data...')
	bank_user = BankLink.query.first()
	if latest:
		first_date = Transaction.query.order_by(Transaction.date.desc()).first().date
	else:
		first_date = datetime.today() - timedelta(days=365 * 7)
	bank_user.retrieve_data(CREDENTIALS['encryptionkey'], first_date, datetime.today(), force)

	db.session.commit()

	info('Processing data... (' + str(Transaction.query.count()) + ' transactions)')
	process_transactions.update_all(False)

	db.session.commit()
