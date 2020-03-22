from datetime import datetime
from typing import TYPE_CHECKING

from ...database import db
from ..base import BaseModel

if TYPE_CHECKING:
	from .transaction import Transaction


class TransactionImported(BaseModel):
	id = db.Column(db.Integer, db.ForeignKey("transaction.id", ondelete="CASCADE"), primary_key=True)
	amount = db.Column(db.Float, nullable=False)
	date = db.Column(db.DateTime, nullable=False)
	info = db.Column(db.Text, nullable=True)

	def __init__(self, transaction: "Transaction", amount: float, date: datetime, info: str):
		self.id = transaction.id
		self.amount = amount
		self.date = date
		self.info = info
