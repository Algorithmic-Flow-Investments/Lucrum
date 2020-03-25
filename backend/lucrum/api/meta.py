from werkzeug.datastructures import MultiDict

from lucrum.models import Transaction


def stats(query: MultiDict):
	latest = Transaction.query.order_by(Transaction.date.desc()).first()
	return {'transactions': Transaction.query.count(), 'latest': latest.date if latest is not None else None}
