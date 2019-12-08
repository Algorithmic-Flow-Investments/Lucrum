from datetime import timedelta, datetime

from models import Account


def show_list():
	accounts = [account.data_basic() for account in Account.query.all()]

	for acc in accounts:
		account = Account.query.filter_by(id=acc['id']).first()
		graph = {
			date.strftime("%Y-%m-%d"): account.calculated_total(date)
			for date in daterange(account.start, datetime.today(), 7)
		}
		graph[(account.start).strftime("%Y-%m-%d")] = 0
		acc['graph'] = graph
	print(accounts)
	return accounts


def daterange(start_date, end_date, interval=1):
	for n in range(int((end_date - start_date).days) + 1, 0, -interval):
		yield start_date + timedelta(n)
