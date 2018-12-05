from database import db
from transaction import Transaction

class Account(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(80), nullable=False)
	balance = db.Column(db.Float, nullable=False)
	max = db.Column(db.Float, nullable=True)
	min = db.Column(db.Float, nullable=True)
	identifier = db.Column(db.String(80), nullable=True)
	description = db.Column(db.Text, nullable=True)

	bankLink_id = db.Column(db.Integer, db.ForeignKey('bank_link.id'), nullable=True)
	bankLink = db.relationship('BankLink', backref=db.backref('accounts', lazy=True), foreign_keys=[bankLink_id])

	def __init__(self, name, identifier=None, description=None):
		self.name = name
		self.identifier = identifier
		self.description = description
		self.balance = 0

	def __repr__(self):
		return '<Account "' + self.name + '">'

	def data_basic(self):
		return {'name': self.name, 'balance': self.balance, 'id': self.id, 'description': self.description}

	def update(self, data):
		print(self.name, data)
		self.balance = data['balance']
		for transaction in data['transactions']:
			if Transaction.query.filter_by(raw_info=transaction['info'], account_id=self.id).first() is None:
				t = Transaction(self, transaction['amount'], transaction['date'], info=transaction['info'])
				print("Added {}".format(t))
				db.session.add(t)
			else:
				print("Skipped <<{}>>".format(transaction['info']))
		db.session.commit()