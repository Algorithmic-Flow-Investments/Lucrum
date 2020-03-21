from dateutil.parser import parse
from werkzeug.datastructures import MultiDict

from models import ScheduledTransaction
from .transactions_common import transactions_find


def scheduled_transaction_list(query: MultiDict):
	min_date = parse(query.get('min', '1970-01-01'))
	max_date = parse(query.get('max', '2100-01-01'))

	transactions_query = transactions_find(ScheduledTransaction, query)  #.filter(
	#or_(ScheduledTransaction.end_date >= min_date, ScheduledTransaction.end_date == None))

	transactions = []
	transaction: ScheduledTransaction
	for transaction in transactions_query.all():
		transactions.extend(transaction.get_occurrences(min_date, max_date))

	return transactions


def get(transaction_id: int):
	return ScheduledTransaction.query.filter(ScheduledTransaction.id == transaction_id).first().data_extra()
