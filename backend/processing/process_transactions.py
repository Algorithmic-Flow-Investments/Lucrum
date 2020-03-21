from multiprocessing import Process, Value
from threading import Thread
from time import sleep
from typing import List

from app_basic import basic_app
from database import db
from models import Transaction
from processing.task_queue import EventManager
from processing.transaction_processors import process_date, process_method, process_target
from logging import warn, info


class ProgressTracker:
	def __init__(self, ) -> None:
		self.updated: List[int] = []
		self.progress = Value('d', 0.0)
		self.progress.value = 0
		t = Thread(target=self._wait_to_send, daemon=True)
		t.start()

	def wait(self, timeout: int = 120, delay: float = 0.5) -> List[int]:
		countdown = timeout / delay
		while self.progress.value < 1:
			sleep(delay)
			countdown -= 1
			if countdown <= 0 and timeout > -1:
				warn("Process tracker timed out", self.progress)
				raise TimeoutError()
		return self.updated

	def _wait_to_send(self) -> None:
		try:
			self.wait()
			self._send()
		except TimeoutError:
			return

	def _send(self):
		EventManager.putTransactionsUpdatedEvent(self.updated)

	def add_updated(self, updated: List[int]):
		self.updated.extend(updated)

	def set_progress(self, value):
		self.progress.value = value
		info(f"Update progress: {round(self.progress.value * 100)}", )


def update_all(threaded: bool = True) -> ProgressTracker:
	info("Updating all transactions...")
	tracker = ProgressTracker()
	if threaded:
		p = Process(target=_update_all, args=(tracker, ))
		p.start()
	else:
		_update_all(tracker)
	return tracker


def _update_all(tracker: ProgressTracker):
	with basic_app().app_context():
		db.reflect()
		pages = Transaction.query.paginate(0, 100, False).pages
	for i in range(pages + 1):
		tracker.add_updated(update_transactions(i, 100))
		tracker.set_progress(i / pages)
	info("Updated all transaction")
	with basic_app().app_context():
		updated = [Transaction.query.filter(Transaction.id == t).first() for t in tracker.updated]
		info(f"Transactions updated: {updated}")


def update_transactions(page=0, per_page=100):
	with basic_app().app_context():
		transactions = Transaction.query.paginate(page, per_page, False).items
		updated = update_transactions_list(transactions)
	return updated


def update_transactions_list(transactions: List[Transaction], standalone: bool = False) -> List[int]:
	updated: List[int] = []
	for transaction in transactions:
		changed = process_transaction(transaction)
		if changed:
			updated.append(transaction.id)
	if standalone:
		EventManager.putTransactionsUpdatedEvent(updated)
	return updated


def process_transaction(transaction: Transaction):
	changed = False
	if transaction.info is not None:
		changed = changed or process_method(transaction)
		changed = changed or process_target(transaction)
		changed = changed or process_date(transaction)
		db.session.commit()
		return changed


if __name__ == "__main__":
	update_all()
