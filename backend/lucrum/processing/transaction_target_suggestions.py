from datetime import timedelta
from typing import List

from sqlalchemy import or_

from lucrum.models import Transaction, Target


def nearby_transactions(transaction: Transaction):
	date_allowance = or_(Transaction.date == transaction.date, Transaction.date == transaction.date + timedelta(1),
							Transaction.date == transaction.date - timedelta(1))
	transactions = Transaction.query.filter(Transaction.amount == -transaction.amount, date_allowance,
											Transaction.account != transaction.account).all()

	for t in transactions:
		yield {'target_id': t.account.target_id, 'reason': {'type': 'nearby_transaction', 'transaction_id': t.id}}


def match_words(transaction: Transaction):
	targets: List[Target] = Target.query.all()
	info = transaction.info.lower().replace(".", " ").replace(",", " ").replace("*", " ").replace("card", "").replace(
		"the", "").replace("payment", "").replace("rate", "")
	info = ''.join([s for s in info if not s.isdigit()])
	words = info.split(" ")
	words = [w for w in words if len(w) > 2]
	for word in words:
		for target in targets:
			if target.name.lower().find(word) != -1 and word != "":
				yield {'target_id': target.id, 'reason': {'type': 'matched_word', 'word': word}}


def process_suggestions(transaction: Transaction):
	nt = list(nearby_transactions(transaction))
	mw = list(match_words(transaction))
	return nt + mw
