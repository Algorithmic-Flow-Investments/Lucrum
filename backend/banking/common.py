import os
from qifparse.parser import QifParser, Transaction
import codecs


class BankAccount:
	def __init__(self, name, identifier, user):
		self.name = name
		self.identifier = identifier
		self.user = user
		self.driver = self.user.driver

	def get_transactions(self):
		self.user.go_home()
		return decode_qif()


def decode_qif():
	file_name = 'tmp/' + os.listdir('tmp')[0]
	with codecs.open(file_name, "r", encoding='utf-8', errors='ignore') as f:
		qif = QifParser.parse(f)
	transactions = [{'date': transaction.date, 'amount': transaction.amount, 'info': transaction.payee} for transaction in qif.get_transactions()[0]]
	os.remove(file_name)
	return transactions
