from dateutil.parser import parse
from werkzeug.datastructures import MultiDict

from .scheduled import scheduled_transaction_list
from .transactions_common import transactions_find, filter_budget, \
 filter_no_internal
from ..database import db
from lucrum.models import Transaction, Category, Tag
from typing import Dict
from ..processing.process_transactions import process_transactions_list
from ..utils import date_range


def transactions_list(query: MultiDict):
	min_date = parse(query.get('min', '1970-01-01'))
	max_date = parse(query.get('max', '2100-01-01'))

	transactions_query = transactions_find(Transaction,
											query).filter(Transaction.date >= min_date,
															Transaction.date <= max_date).order_by(Transaction.date.desc())
	transactions = transactions_query.all()
	transactions.extend(scheduled_transaction_list(query))
	return [transaction.data_basic() for transaction in transactions]


def stats(query: MultiDict):
	min_date = parse(query.get('min', '1970-01-01'))
	max_date = parse(query.get('max', '2100-01-01'))
	budget_id = query.get('budget_id', 1)
	transactions_base_query = filter_budget(Transaction, Transaction.query, budget_id)
	transactions_base_query = filter_no_internal(transactions_base_query)
	transactions_query = transactions_base_query.filter(Transaction.date >= min_date, Transaction.date <= max_date)
	return {'total': stats_total(transactions_query)}


def stats_total(transactions_query):
	# noinspection PyTypeChecker
	return {
		'gross': sum(transaction.amount for transaction in transactions_query.all()),
		'income': sum(transaction.amount for transaction in transactions_query.filter(Transaction.amount > 0).all()),
		'outgoing': -sum(transaction.amount for transaction in transactions_query.filter(Transaction.amount < 0).all())
	}


def graph(query: MultiDict):
	min_date = parse(query.get('min', '1970-01-01'))
	max_date = parse(query.get('max', '2100-01-01'))
	budget_id = query.get('budget_id', 1)
	graph_data = []
	# noinspection PyTypeChecker
	transaction_query = filter_budget(Transaction, Transaction.query, budget_id).filter(Transaction.amount < 0)
	if (max_date - min_date).days <= 31:
		for date in date_range(min_date, max_date):
			graph_data.append({
				'amount':
				round(-sum(transaction.amount
							for transaction in transaction_query.filter(Transaction.date == date).all())),
				'date':
				date.day
			})
	else:
		pass  # year

	return graph_data


def tags_categories(query: MultiDict):
	min_date = parse(query.get('min', '1970-01-01'))
	max_date = parse(query.get('max', '2100-01-01'))
	budget_id = query.get('budget_id', 1)
	transactions_query = filter_budget(Transaction, Transaction.query,
										budget_id).filter(Transaction.date >= min_date, Transaction.date <= max_date)
	transactions = transactions_query.all()

	categories = {
		category.id: {
			'total': {
				'gross': 0,
				'income': 0,
				'outgoing': 0
			},
			'tags': {tag.id: {
				'gross': 0,
				'income': 0,
				'outgoing': 0
			}
						for tag in category.tags}
		}
		for category in Category.query.all()
	}
	categories[-1] = {
		'total': {
			'gross': 0,
			'income': 0,
			'outgoing': 0
		},
		'tags':
		{tag.id: {
			'gross': 0,
			'income': 0,
			'outgoing': 0
		}
			for tag in Tag.query.filter(Tag.category_id.is_(None)).all()}
	}

	for transaction in transactions:
		split_amount = round(transaction.amount / len(transaction.tags), 2) if transaction.tags else 0
		for tag in transaction.tags:
			category = tag.category_id if tag.category_id is not None else -1

			if split_amount < 0:
				categories[category]['total']['outgoing'] += -split_amount
				categories[category]['tags'][tag.id]['outgoing'] += -split_amount
			else:
				categories[category]['total']['income'] += split_amount
				categories[category]['tags'][tag.id]['income'] += split_amount

			categories[category]['total']['gross'] += split_amount
			categories[category]['tags'][tag.id]['gross'] += split_amount
	return categories


def get(transaction_id: int):
	return Transaction.query.filter(Transaction.id == transaction_id).first().data_extra()


def process(query: MultiDict):
	min_date = parse(query.get('min', '1970-01-01'))
	max_date = parse(query.get('max', '2100-01-01'))
	transactions = Transaction.query.filter(Transaction.date >= min_date, Transaction.date <= max_date).all()
	process_transactions_list(transactions, True)
	return "PENDING"


def update(transaction_id: int, data: Dict):
	transaction = Transaction.query.filter(Transaction.id == transaction_id).one()
	for key, value in data.items():
		if key == 'target_id':
			if transaction.target_id != value:
				transaction.set_target(value)

		if key == 'method_id':
			if transaction.method_id != value:
				transaction.set_method(value)

		if key == 'parent_id':
			transaction.parent_transaction_id = value
	db.session.commit()
	return transaction.data_extra()
