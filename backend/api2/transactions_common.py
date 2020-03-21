from dateutil.parser import parse
from sqlalchemy.sql.expression import or_
from werkzeug.datastructures import MultiDict

from models import Transaction, Tag, Category, Budget, Target
from utils import date_range


def transactions_find(model, query: MultiDict):
	min_date = parse(query.get('min', '1970-01-01'))
	max_date = parse(query.get('max', '2100-01-01'))
	budget_id = query.get('budget_id', 1)
	target_id = query.get('target_id', None, int)
	category_id = query.get('category_id', None, int)
	tag_id = query.get('tag_id', None, int)

	transactions_query = filter_budget(model, model.query, budget_id)
	if target_id:
		if target_id == -1:
			transactions_query = transactions_query.filter(model.target_id.is_(None))
		else:
			transactions_query = transactions_query.filter(model.target_id == target_id)
	if category_id or tag_id:
		transactions_query = filter_tag_category(transactions_query, tag_id, category_id)
	return transactions_query


def filter_budget(model, query, budget_id: int = 1):
	return query.join(model.tags, isouter=True) \
                                                     .join(Tag.category, isouter=True) \
                                                     .join(Category.budgets, isouter=True) \
                                                     .filter(or_(Budget.id == budget_id, Budget.id.is_(None)))


def filter_tag_category(query, tag_id=None, cat_id=None):
	if cat_id:
		query = query.filter(Category.id == cat_id)
	if tag_id:
		query = query.filter(Tag.id == tag_id)
	return query


def filter_no_internal(query):
	return query.outerjoin(Target, Target.id == Transaction.target_id).filter(
		or_(Transaction.target_id.is_(None), Target.internal_account_id.is_(None)))
