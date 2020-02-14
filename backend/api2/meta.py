from werkzeug.datastructures import MultiDict

from models import Transaction


def stats(query: MultiDict):
	return {
		'transactions': Transaction.query.count(),
		'latest': Transaction.query.order_by(Transaction.date.desc()).first().date
	}
