from werkzeug.datastructures import MultiDict

from lucrum.models import Transaction


def stats(query: MultiDict):
	print(Transaction.query.first())
	return {
		'transactions': Transaction.query.count(),
		'latest': Transaction.query.order_by(Transaction.date.desc()).first().date
	}
