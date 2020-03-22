from werkzeug.datastructures import MultiDict

from lucrum.models import Account


def accounts_list(query: MultiDict):
	accounts = Account.query
	return [account.data_basic() for account in accounts.all()]


def accounts_balance_graph(query: MultiDict):
	accounts = Account.query
	return {account.id: account.balance_graph() for account in accounts.all()}


def get(account_id: int):
	return Account.query.filter(Account.id == account_id).first().data_extra()
