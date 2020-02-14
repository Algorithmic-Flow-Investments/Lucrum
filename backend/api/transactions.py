from datetime import datetime, timedelta

from sqlalchemy import or_

from models import Budget, Category
from models.tag import Tag
from models.transaction import Transaction, Target


def filter_budget(query, budget_id: int = 1):
	return query.filter(
		or_(Transaction.target == None, Transaction.target.has(Target.internal_account == None))) \
                  .join(Transaction.tags, isouter=True)\
                  .join(Tag.category, isouter=True)\
                  .join(Category.budgets, isouter=True)\
                  .filter(Budget.id == budget_id)


def tbr(budget_id: int = 1):
	return filter_budget(Transaction.query, budget_id)


def show_list(minDate, maxDate, targetID=None, idOnly=False):
	transactions = Transaction.query.filter(Transaction.date >= minDate,
											Transaction.date <= maxDate).order_by(Transaction.date.desc())
	if targetID:
		if targetID == -1:
			transactions = transactions.filter(Transaction.target_id == None)
		else:
			transactions = transactions.filter(Transaction.target_id == targetID)

	if idOnly:
		return [transaction.id for transaction in transactions.all()]

	return [transaction.data() for transaction in transactions.all()]


def stats(min_date: datetime, max_date: datetime, budget_id: int = 1):
	transactions_base_query = tbr(budget_id)
	transactions_query = transactions_base_query.filter(Transaction.date >= min_date, Transaction.date <= max_date)
	date_diff = max_date - min_date

	prev_range_transactions_query = transactions_base_query.filter(Transaction.date >= min_date - date_diff,
																	Transaction.date <= max_date - date_diff)
	prev_all_transactions_query = transactions_base_query.filter(Transaction.date <= min_date)

	first_transaction = prev_all_transactions_query.order_by(Transaction.date.asc()).first()  # type: Transaction
	ranges_in_all = (min_date - first_transaction.date) / date_diff if first_transaction is not None else 1

	totals = {
		'transactions': _total(transactions_query),
		'prev_range_transactions': _total(prev_range_transactions_query),
		'prev_all_transactions': _total(prev_all_transactions_query)
	}

	budget = Budget.query.filter_by(id=budget_id).first()

	return {
		'gross':
		_averages('gross', totals, ranges_in_all),
		'income':
		_averages('income', totals, ranges_in_all),
		'outgoing':
		_averages('outgoing', totals, ranges_in_all),
		'first_date':
		transactions_query.order_by(Transaction.date.asc()).first().date
		if transactions_query.count() > 0 else min_date,
		'last_date':
		transactions_query.order_by(Transaction.date.desc()).first().date
		if transactions_query.count() > 0 else max_date,
		'budget':
		budget.stats(),
		'categories':
		tags_categories(min_date, max_date, budget_id)
	}


def _total(transactions_query):
	return {
		'gross': sum(transaction.amount for transaction in transactions_query.all()),
		'income': sum(transaction.amount for transaction in transactions_query.filter(Transaction.amount > 0).all()),
		'outgoing': -sum(transaction.amount for transaction in transactions_query.filter(Transaction.amount < 0).all())
	}


def _averages(cat, totals, divisor=1):
	return {
		'total': totals['transactions'][cat],
		'prev_range_diff': {
			'amount':
			totals['transactions'][cat] - totals['prev_range_transactions'][cat],
			'percent': (totals['transactions'][cat] - totals['prev_range_transactions'][cat]) /
			totals['prev_range_transactions'][cat] * 100 if totals['prev_range_transactions'][cat] > 0 else 100
		},
		'prev_all_diff': {
			'amount':
			totals['transactions'][cat] - totals['prev_all_transactions'][cat] / divisor,
			'percent': (totals['transactions'][cat] - totals['prev_all_transactions'][cat]) /
			totals['prev_all_transactions'][cat] * 100 / divisor if totals['prev_all_transactions'][cat] > 0 else 100
		}
	}


def daterange(start_date, end_date):
	for n in range(int((end_date - start_date).days) + 1):
		yield start_date + timedelta(n)


def graph(min_date: datetime, max_date: datetime, budget: int = 1):
	"""

	Transaction.query.filter(or_(Transaction.target == None, Transaction.target.has(Target.internal_account == None)))\
		.outerjoin(Transaction.tags).filter(or_(Tag.exclude == False, Tag.exclude == None))
	"""
	graph_data = []
	transaction_query = tbr(budget).filter(Transaction.amount < 0)
	if (max_date - min_date).days <= 31:
		for date in daterange(min_date, max_date):
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


def tags_categories(min_date: datetime, max_date: datetime, budget: int = 1):
	transactions = tbr(budget).filter(Transaction.date >= min_date, Transaction.date <= max_date).all()
	categories = {
		category.name: {
			'total': 0,
			'tags': {tag.name: {
				'total': 0
			}
						for tag in category.tags}
		}
		for category in Category.query.all()
	}
	categories['Misc'] = {
		'total': 0,
		'tags': {tag.name: {
			'total': 0
		}
					for tag in Tag.query.filter(Tag.category_id == None).all()}
	}
	for transaction in transactions:
		split_amount = round(transaction.amount / len(transaction.tags), 2)
		for tag in transaction.tags:
			category = tag.category.name if tag.category is not None else 'Misc'
			categories[category]['total'] += split_amount
			categories[category]['tags'][tag.name]['total'] += split_amount

	return categories
