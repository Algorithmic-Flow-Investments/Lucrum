from datetime import datetime

import plaid

from api_keys import PLAID_CLIENT_ID, PLAID_SECRET, PLAID_PUBLIC_KEY
PLAID_ENV = 'development'
PLAID_PRODUCTS = 'auth,transactions'
PLAID_COUNTRY_CODES = 'GB'
PLAID_OAUTH_REDIRECT_URI = ''
PLAID_OAUTH_NONCE = ''

client = plaid.Client(client_id=PLAID_CLIENT_ID,
						secret=PLAID_SECRET,
						public_key=PLAID_PUBLIC_KEY,
						environment=PLAID_ENV,
						api_version='2019-05-29')


def get_transactions(access_token, start_date: datetime, end_date: datetime):
	transactions = []
	while True:
		response = client.Transactions.get(access_token,
											'{:%Y-%m-%d}'.format(start_date),
											'{:%Y-%m-%d}'.format(end_date),
											offset=len(transactions))
		transactions.extend(response['transactions'])
		if len(transactions) >= response['total_transactions']:
			return transactions


def get_balance(access_token):
	return client.Accounts.balance.get(access_token)['accounts']
