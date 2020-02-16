import signal
from multiprocessing.pool import AsyncResult
from time import sleep
from typing import List

from database import db
from models import Transaction, MethodString, TargetString, Target
from processing.task_queue import EventManager
from app import create_app
from multiprocessing import Pool, cpu_count, Process, Value, Array
from threading import Thread
import os

import code, traceback, signal


class ProgressTracker:
	def __init__(self, updated=[]):
		self.updated = updated
		self.progress = Value('d', 0.0)
		if updated:
			self.progress.value = 1
			self._send()
		else:
			self.progress.value = 0
			t = Thread(target=self._wait_to_send, daemon=True)
			t.start()

	def wait(self, timeout=30, delay=0.5):
		countdown = timeout / delay
		while self.progress.value < 1:
			sleep(delay)
			countdown -= 1
			if countdown <= 0:
				print("Process tracker timed out", self.progress)
				raise TimeoutError()
		return self.updated

	def _wait_to_send(self):
		results = self.wait()
		results = [t for sub in results for t in sub]

	def _send(self):
		EventManager.putTransactionsUpdatedEvent(self.updated)

	def add_updated(self, updated: List[Transaction]):
		self.updated.extend(updated)

	def set_progress(self, value):
		self.progress.value = value


def update_all(threaded=True):
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


def update_transactions(page=0, perpage=100):
	with create_app().app_context():
		transactions = Transaction.query.paginate(page, perpage, False).items
		updated = update_transactions_list(transactions)
	return updated


def update_transactions_list(transactions, standalone=False):
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
		db.session.commit()
		# print("end   transaction", transaction.id)
		return changed


def process_method(transaction: Transaction):
	if transaction.manual_method:
		return False
	old = transaction.method_id
	raw = transaction.info.lower()
	for methodStr in MethodString.query.all():
		if raw.find(methodStr.string) != -1:
			transaction.method_id = methodStr.parent.id
			return transaction.method_id != old
	transaction.method_id = None  # TODO: Manual clas
	return False


def process_target(transaction: Transaction):
	if transaction.manual_target:
		return False
	old = transaction.target_id

	internal, different = process_internal(transaction)
	if internal:
		return different

	raw = transaction.info.lower()  # type: str
	split = []
	if raw.find('ref.') != -1:
		split = raw.split('ref.', maxsplit=1)
	elif raw.find('reference') != -1:
		split = raw.split('reference', maxsplit=1)
	if len(split) > 1:
		if split[1].find('from') != -1:
			split2 = split[1].split('from', maxsplit=1)
		else:
			split2 = split[1].split(',', maxsplit=1)
		raw = split[0] + split2[-1]
		transaction.data_auto.reference = split2[0]

	for targetStr in TargetString.query.all():
		if raw.find(targetStr.string) != -1:
			transaction.target_id = targetStr.parent.id
			return transaction.target_id != old

	# If ignoring reference doesn't work, include it
	raw = transaction.info.lower()
	for targetStr in TargetString.query.all():
		if raw.find(targetStr.string) != -1:
			transaction.target_id = targetStr.parent.id
			return transaction.target_id != old

	transaction.target_id = None  # TODO: Manual clas
	return old is not None


def process_internal(transaction: Transaction):
	old = transaction.target_id
	mirrored_transaction = Transaction.query.filter(Transaction.amount == -transaction.amount,
													Transaction.date == transaction.date,
													Transaction.account != transaction.account).first()
	if mirrored_transaction:
		this_account_target = Target.query.filter_by(name=transaction.account.name).first()
		other_account_target = Target.query.filter_by(name=mirrored_transaction.account.name).first()
		if this_account_target and other_account_target:
			mirrored_transaction.target = this_account_target
			transaction.target = other_account_target
			return True, transaction.target_id != old
	return False, transaction.target_id != old


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
