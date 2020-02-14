from dateutil.parser import parse
from werkzeug.datastructures import MultiDict
from models import Method


def methods_list(query: MultiDict):
	methods = Method.query
	return [method.data_basic() for method in methods.all()]
