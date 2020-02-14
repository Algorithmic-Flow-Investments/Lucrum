from werkzeug.datastructures import MultiDict

from models import Budget


def budgets_list(query: MultiDict):
	return [budget.data_basic() for budget in Budget.query.all()]
