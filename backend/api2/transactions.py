from datetime import timedelta

from dateutil.parser import parse
from werkzeug.datastructures import MultiDict

from database import db
from models import Transaction, Target, Tag, Category, Budget, Dict
from sqlalchemy import or_

from processing.process_transactions import update_transactions_list


def transactions_list(query: MultiDict):
	min_date = parse(query.get('min', '1970-01-01'))
	max_date = parse(query.get('max', '2100-01-01'))
	budget_id = query.get('budget_id', 1)
	target_id = query.get('target_id', None, int)
	category_id = query.get('category_id', None, int)
	tag_id = query.get('tag_id', None, int)

	transactions_query = filter_budget(Transaction.query,
										budget_id).filter(Transaction.date >= min_date,
															Transaction.date <= max_date).order_by(Transaction.date.desc())
	if target_id:
		if target_id == -1:
			transactions_query = transactions_query.filter(Transaction.target_id == None)
		else:
			transactions_query = transactions_query.filter(Transaction.target_id == target_id)
	if category_id or tag_id:
		transactions_query = filter_tag_category(transactions_query, tag_id, category_id)
	return [transaction.data_basic() for transaction in transactions_query.all()]


def filter_budget(query, budget_id: int = 1):
	return query.join(Transaction.tags, isouter=True)\
                                                              .join(Tag.category, isouter=True)\
                                                              .join(Category.budgets, isouter=True)\
                                                              .filter(or_(Budget.id == budget_id, Budget.id == None))
	# .filter(or_(Transaction.target == None, Transaction.target.has(Target.internal_account == None))) \


def filter_tag_category(query, tag_id=None, cat_id=None):
	# query = query.join(Transaction.tags, isouter=True)\
	#        .join(Tag.category, isouter=True)
	if cat_id:
		query = query.filter(Category.id == cat_id)
	if tag_id:
		query = query.filter(Tag.id == tag_id)
	return query


def tbr(budget_id: int = 1):
	return filter_budget(Transaction.query, budget_id)


def stats(query: MultiDict):
	min_date = parse(query.get('min', '1970-01-01'))
	max_date = parse(query.get('max', '2100-01-01'))
	budget_id = query.get('budget_id', 1)
	transactions_base_query = tbr(budget_id).filter(
		or_(Transaction.target == None, Transaction.target.has(Target.internal_account == None)))
	transactions_query = transactions_base_query.filter(Transaction.date >= min_date, Transaction.date <= max_date)
	return {'total': _total(transactions_query)}


def daterange(start_date, end_date):
	for n in range(int((end_date - start_date).days) + 1):
		yield start_date + timedelta(n)


def graph(query: MultiDict):
	"""

	Transaction.query.filter(or_(Transaction.target == None, Transaction.target.has(Target.internal_account == None)))\
		.outerjoin(Transaction.tags).filter(or_(Tag.exclude == False, Tag.exclude == None))
	"""
	min_date = parse(query.get('min', '1970-01-01'))
	max_date = parse(query.get('max', '2100-01-01'))
	budget_id = query.get('budget_id', 1)
	graph_data = []
	transaction_query = tbr(budget_id).filter(Transaction.amount < 0)
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


def _total(transactions_query):
	return {
		'gross': sum(transaction.amount for transaction in transactions_query.all()),
		'income': sum(transaction.amount for transaction in transactions_query.filter(Transaction.amount > 0).all()),
		'outgoing': -sum(transaction.amount for transaction in transactions_query.filter(Transaction.amount < 0).all())
	}


def get(transaction_id: int):
	return Transaction.query.filter(Transaction.id == transaction_id).first().data_extra()


def process(query: MultiDict):
	min_date = parse(query.get('min', '1970-01-01'))
	max_date = parse(query.get('max', '2100-01-01'))
	transactions = Transaction.query.filter(Transaction.date >= min_date, Transaction.date <= max_date).all()
	update_transactions_list(transactions, True)
	return "PENDING"


def update(transaction_id: int, data: Dict):
	transaction = Transaction.query.filter(Transaction.id == transaction_id).one()
	for key, value in data.items():
		if key == 'target_id':
			transaction.target_id = value

		if key == 'method_id':
			transaction.method_id = value

		if key == 'parent_id':
			transaction.parent_transaction_id = value

		if key == 'manual_target':
			if value is not None:
				transaction.manual_target = value
	db.session.commit()
	return transaction.data_extra()


def tags_categories(query: MultiDict):
	min_date = parse(query.get('min', '1970-01-01'))
	max_date = parse(query.get('max', '2100-01-01'))
	budget_id = query.get('budget_id', 1)
	transactions_query = tbr(budget_id).filter(Transaction.date >= min_date, Transaction.date <= max_date)
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
			for tag in Tag.query.filter(Tag.category_id == None).all()}
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
