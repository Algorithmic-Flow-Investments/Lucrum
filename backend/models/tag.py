from database import db
from models import Target


class Tag(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(80), nullable=False)
	manual_transactions = db.relationship('Transaction', secondary='transaction_tags')
	targets = db.relationship('Target', secondary='target_tags')
	exclude = db.Column(db.Boolean)

	def __init__(self, name):
		self.name = name
		self.exclude = False

	def __repr__(self):
		return '<Tag "' + self.name + '">'

	def data_basic(self):
		return {'name': self.name, 'id': self.id}

	def data_advanced(self, transaction):
		return {'name': self.name, 'id': self.id}


target_tags = db.Table('target_tags',
	db.Column('tag_id', db.Integer, db.ForeignKey(Tag.id)),
	db.Column('target_id', db.Integer, db.ForeignKey(Target.id))
)

transaction_tags = db.Table('transaction_tags',
	db.Column('tag_id', db.Integer, db.ForeignKey(Tag.id)),
	db.Column('transaction_id', db.Integer, db.ForeignKey('transaction.id'))
)
