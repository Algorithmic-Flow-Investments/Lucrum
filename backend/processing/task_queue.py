from multiprocessing import Queue
from json import dumps
from queue import Empty
from sys import getrefcount
from typing import List

from database import db
from models import Transaction, Target
from app import create_app


class Event:
	pass


class TransactionsUpdatedEvent(Event):
	def __init__(self, transactions: List[int]):
		super().__init__()
		self.transactions = transactions

	def toJSON(self):
		return dumps({"event": "TRANSACTIONS_UPDATED", "value": self.transactions})


class TargetsUpdatedEvent(Event):
	def __init__(self, targets: List[Target]):
		super().__init__()
		self.targets = targets

	def toJSON(self):
		return dumps({"event": "TARGETS_UPDATED", "value": self.targets})


class HeartbeatEvent(Event):
	def __init__(self):
		super().__init__()

	def toJSON(self):
		return dumps({"event": "HEARTBEAT"})


class ConnectedEvent(Event):
	def __init__(self):
		super().__init__()

	def toJSON(self):
		return dumps({"event": "CONNECTED"})


class EventManager:
	connections = []

	@staticmethod
	def new_connection():
		con = EventConnection()
		EventManager.connections.append(con)
		return con

	@staticmethod
	def put(event: Event):
		for connection in EventManager.connections:
			print(connection, getrefcount(connection))
			connection.put(event)

	@staticmethod
	def close(con):
		EventManager.connections.remove(con)

	@staticmethod
	def putTransactionsUpdatedEvent(transactions: List[Transaction]):
		EventManager.put(TransactionsUpdatedEvent([transaction.id for transaction in transactions]))

	@staticmethod
	def putTargetsUpdatedEvent(targets: List[Target]):
		EventManager.put(TargetsUpdatedEvent([target.id for target in targets]))

	@staticmethod
	def putHeartbeatEvent():
		EventManager.put(HeartbeatEvent())

	@staticmethod
	def putConnectedEvent():
		EventManager.put(ConnectedEvent())


class EventConnection:
	def __init__(self):
		self.queue = Queue()

	def get_stream(self):
		self.queue.put(ConnectedEvent())
		try:
			while True:
				try:
					with create_app().app_context():
						yield "data:" + self.queue.get(timeout=5).toJSON() + "\n\n"
				except Empty:
					self.queue.put(HeartbeatEvent())
				except EOFError:
					self.queue.put(HeartbeatEvent())
		except GeneratorExit:
			EventManager.close(self)

	def put(self, event: Event):
		self.queue.put(event)
