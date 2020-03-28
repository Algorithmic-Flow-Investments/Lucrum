from datetime import datetime

from dateutil.parser import parse
from werkzeug.datastructures import MultiDict

from lucrum.models import Account


def accounts_list(query: MultiDict):
	accounts = Account.query
	return [account.data_basic() for account in accounts.all()]


def accounts_balance_graph(query: MultiDict):
	accounts = Account.query
	min_date = parse(query.get('min', '1970-01-01'))
	if min_date < datetime(2017, 1, 1):
		min_date = datetime(2017, 1, 1)
	max_date = parse(query.get('max', '2100-01-01'))
	return {account.id: account.balance_graph(min_date, max_date) for account in accounts.all()}


def get(account_id: int):
	return Account.query.filter(Account.id == account_id).first().data_extra()
