import os
from qifparse.parser import QifParser, Transaction

class BankAccount():
	def __init__(self, name, identifier, user):
		self.name = name
		self.identifier = identifier
		self.user = user
		self.driver = self.user.driver

	@property
	def id(self):
		return self.sort_code, self.account_no

	def get_transactions(self):
		self.user.go_home()
		return decodeQif()

def decodeQif():
	with open('tmp/' + os.listdir('tmp')[0]) as f:
		qif = QifParser.parse(f)
	transactions = [{'date': transaction.date, 'amount': transaction.amount, 'info': transaction.payee} for transaction in qif.get_transactions()[0]]
	os.remove('tmp/' + os.listdir('tmp')[0])
	return transactions