from database import db
from datetime import datetime


class TransactionInferred(db.Model):
	id = db.Column(db.Integer, db.ForeignKey("transaction.id"), primary_key=True)
	date = db.Column(db.DateTime)
	reference = db.Column(db.Text)

	target_id = db.Column(db.Integer, db.ForeignKey('target.id', ondelete='SET NULL'))
	target = db.relationship('Target', foreign_keys=[target_id])

	method_id = db.Column(db.Integer, db.ForeignKey('method.id'))
	method = db.relationship('Method', foreign_keys=[method_id])

	tags = db.relationship(
		'Tag',
		secondary='join(Target, target_tags, target_tags.c.target_id == Target.id).'
		'join(Tag, target_tags.c.tag_id == Tag.id).join(Transaction, Transaction.target_id == Target.id)',
		primaryjoin='TransactionInferred.id == Transaction.id')

	# primaryjoin='TransactionInferred.target_id==target_tags.c.target_id')

	# tags = db.relationship('Tag', secondary='target_tags', primaryjoin='Transaction.target_id==target_tags.c.target_id')

	def __init__(self, transaction: "Transaction"):
		#, date: datetime, reference: str, target: "Target", method: "Method"
		self.id = transaction.id
		# self.date = date
		# self.reference = reference
		# self.target_id = target.id
		# self.method_id = method.id
