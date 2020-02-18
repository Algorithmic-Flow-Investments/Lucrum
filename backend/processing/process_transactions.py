from multiprocessing import Process, Value
from threading import Thread
from time import sleep
from typing import List

from app import create_app
from database import db
from models import Transaction
from processing.task_queue import EventManager
from processing.transaction_processors import process_date, process_method, process_target, process_internal


class ProgressTracker:
	def __init__(self, updated=None) -> None:
		if updated is None:
			updated = []
		self.updated = updated
		self.progress = Value('d', 0.0)
		if updated:
			self.progress.value = 1
			self._send()
		else:
			self.progress.value = 0
			t = Thread(target=self._wait_to_send, daemon=True)
			t.start()

	def wait(self, timeout: int = 30, delay: float = 0.5) -> List[Transaction]:
		countdown = timeout / delay
		while self.progress.value < 1:
			sleep(delay)
			countdown -= 1
			if countdown <= 0:
				print("Process tracker timed out", self.progress)
				raise TimeoutError()
		return self.updated

	def _wait_to_send(self) -> None:
		results = self.wait()
		results = [t for sub in results for t in sub]

	def _send(self):
		EventManager.putTransactionsUpdatedEvent(self.updated)

	def add_updated(self, updated: List[Transaction]):
		self.updated.extend(updated)

	def set_progress(self, value):
		self.progress.value = value


def update_all(threaded: bool = True) -> ProgressTracker:
	print("Updating all transactions...")
	tracker = ProgressTracker()
	if threaded:
		p = Process(target=_update_all, args=(tracker, ))
		p.start()
	else:
		_update_all(tracker)
	return tracker


def _update_all(tracker: ProgressTracker):
	with create_app().app_context():
		pages = Transaction.query.paginate(0, 100, False).pages
		for i in range(pages + 1):
			tracker.add_updated(update_transactions(i, 100))
			tracker.set_progress(i / pages)
		print("Updated all")
		print("Updated:", tracker.updated)


def update_transactions(page=0, per_page=100):
	with create_app().app_context():
		transactions = Transaction.query.paginate(page, per_page, False).items
		updated = update_transactions_list(transactions)
	return updated


def update_transactions_list(transactions: List[Transaction], standalone: bool = False) -> List[Transaction]:
	updated = []
	for transaction in transactions:
		changed = process_transaction(transaction)
		if changed:
			updated.append(transaction)
	if standalone:
		print("Special send event", updated)
		EventManager.putTransactionsUpdatedEvent(updated)
	return updated


def process_transaction(transaction: Transaction):
	changed = False
	if transaction.info is not None:
		# print("start transaction", transaction.id)
		changed = changed or process_method(transaction)
		changed = changed or process_target(transaction)
		changed = changed or process_date(transaction)
		db.session.commit()
		# print("end   transaction", transaction.id)
		return changed


if __name__ == "__main__":
	update_all()

#
# if __name__ == "__main__":
# 	event_queue.put(Event(EventType.TRANSACTIONS_UPDATED, 123))
# 	with create_app().app_context():
# 		# t = Transaction.query.filter(Transaction.id == 1235).first()  #type: Transaction
# 		# print(t)
# 		# process_transaction(t)
# 		# print(t)
#
# 		# t.target_id = None
# 		# db.session.commit()
# 		# print(t)
# 		# r = process_transaction(t)
# 		# print("d", r)
#
# 		ts = TargetString.query.filter(TargetString.string == "southern water service").first()
# 		if ts:
# 			db.session.delete(ts)
# 		else:
# 			t = Target.query.filter(Target.id == 139).first()
# 			ts = TargetString(t, "southern water service")
# 		db.session.commit()
# 	update_all()
# 	sleep(1000)
