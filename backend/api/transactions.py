from functools import reduce

from models.transaction import Transaction, Target
from models.tag import Tag
from datetime import datetime, timedelta
from typing import List
from sqlalchemy import or_, not_


def tbr():
	return Transaction.query.filter(or_(Transaction.target == None, Transaction.target.has(Target.internal_account == None)))\
		.outerjoin(Transaction.tags).filter(or_(Tag.exclude == False, Tag.exclude == None))


def show_list(minDate, maxDate):
	transactions = Transaction.query.filter(Transaction.date >= minDate, Transaction.date <= maxDate).order_by(Transaction.date.desc()).all()
	return [transaction.data() for transaction in transactions]


def stats(min_date: datetime, max_date: datetime):
	transactions_base_query = tbr()
	print(transactions_base_query.all())
	transactions_query = transactions_base_query.filter(Transaction.date >= min_date, Transaction.date <= max_date)
	date_diff = max_date - min_date

	prev_range_transactions_query = transactions_base_query.filter(Transaction.date >= min_date - date_diff, Transaction.date <= max_date - date_diff)
	prev_all_transactions_query = transactions_base_query.filter(Transaction.date <= min_date)

	first_transaction = prev_all_transactions_query.order_by(Transaction.date.asc()).first()  # type: Transaction
	ranges_in_all = (min_date - first_transaction.date) / date_diff if first_transaction is not None else 1

	totals = {
		'transactions': _total(transactions_query),
		'prev_range_transactions': _total(prev_range_transactions_query),
		'prev_all_transactions': _total(prev_all_transactions_query)
	}

	return {
		"gross": _averages("gross", totals, ranges_in_all),
		"income": _averages("income", totals, ranges_in_all),
		"outgoing": _averages("outgoing", totals, ranges_in_all),
		"first_date": transactions_query.order_by(Transaction.date.asc()).first().date,
		"last_date": transactions_query.order_by(Transaction.date.desc()).first().date
	}


def _total(transactions_query):
	return {
		"gross": sum(transaction.amount for transaction in transactions_query.all()),
		"income": sum(transaction.amount for transaction in transactions_query.filter(Transaction.amount > 0).all()),
		"outgoing": -sum(transaction.amount for transaction in transactions_query.filter(Transaction.amount < 20).all())
	}


def _averages(cat, totals, divisor=1):
	return {
		"total": totals['transactions'][cat],
		"prev_range_diff": {
			"amount": totals['transactions'][cat] - totals['prev_range_transactions'][cat],
			"percent": (totals['transactions'][cat] - totals['prev_range_transactions'][cat]) / totals['prev_range_transactions'][cat] * 100 if totals['prev_range_transactions'][cat] > 0 else 100
		},
		"prev_all_diff": {
			"amount": totals['transactions'][cat] - totals['prev_all_transactions'][cat] / divisor,
			"percent": (totals['transactions'][cat] - totals['prev_all_transactions'][cat]) / totals[
				'prev_all_transactions'][cat] * 100 / divisor if totals['prev_all_transactions'][cat] > 0 else 100
		}
	}


def daterange(start_date, end_date):
	for n in range(int ((end_date - start_date).days)):
		yield start_date + timedelta(n)


def graph(min_date: datetime, max_date: datetime):
	"""

	Transaction.query.filter(or_(Transaction.target == None, Transaction.target.has(Target.internal_account == None)))\
		.outerjoin(Transaction.tags).filter(or_(Tag.exclude == False, Tag.exclude == None))
	"""
	graph_data = []
	transaction_query = tbr().filter(Transaction.amount < 0)
	if (max_date - min_date).days <= 31:
		for date in daterange(min_date, max_date):
			graph_data.append({'amount': round(-sum(transaction.amount for transaction in transaction_query.filter(Transaction.date == date).all())), 'date': date.day})
	else:
		pass # year

	return graph_data