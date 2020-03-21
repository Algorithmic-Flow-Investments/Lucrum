from typing import TYPE_CHECKING

from database import db
from models.base import BaseModel

if TYPE_CHECKING:
	from .transaction import Transaction


class TransactionManual(BaseModel):
	id = db.Column(db.Integer, db.ForeignKey("transaction.id", ondelete="CASCADE"), primary_key=True)
	date = db.Column(db.DateTime)
	reference = db.Column(db.Text)
	amount = db.Column(db.Float)

	target_id = db.Column(db.Integer, db.ForeignKey('target.id', ondelete='SET NULL'))
	target = db.relationship('Target', foreign_keys=[target_id])

	method_id = db.Column(db.Integer, db.ForeignKey('method.id', ondelete='SET NULL'))
	method = db.relationship('Method', foreign_keys=[method_id])

	tags = db.relationship('Tag', secondary='transaction_tags')

	def __init__(self, transaction: "Transaction"):
		# , amount: int, date: datetime, reference: str, target: "Target",
		# 					method: "Method"
		self.id = transaction.id

	# self.amount = amount
	# self.date = date
	# self.reference = reference
	# self.target_id = target.id
	# self.method_id = method.id
