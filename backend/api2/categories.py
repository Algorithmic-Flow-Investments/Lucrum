from werkzeug.datastructures import MultiDict

from models import Category


def categories_list(query: MultiDict):
	categories = Category.query
	return [category.data_basic() for category in categories.all()]
