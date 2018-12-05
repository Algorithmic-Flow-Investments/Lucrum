from database import db
import banking
from simplecrypt import encrypt, decrypt
from werkzeug.security import check_password_hash, generate_password_hash
import datetime
import time


class BankLink(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	bank = db.Column(db.String(80), nullable=False)
	userID = db.Column(db.String(80), nullable=False)
	password = db.Column(db.String(80), nullable=False)
	sec_num = db.Column(db.String(80), nullable=False)
	db_password_hash = db.Column(db.String(80), nullable=False)

	def __init__(self, bank, userID, password, sec_num, dbpassword):
		self.bank = bank
		self.db_password_hash = generate_password_hash(dbpassword)
		self.userID = encrypt(dbpassword, userID.encode('utf8'))
		self.password = encrypt(dbpassword, password.encode('utf8'))
		self.sec_num = encrypt(dbpassword, sec_num.encode('utf8'))

	def check_password(self, dbpassword):
		return check_password_hash(self.db_password_hash, dbpassword)

	def connect(self, dbpassword):
		if not self.check_password(dbpassword):
			return 0
		userID = decrypt(dbpassword, self.userID).decode('utf8')
		password = decrypt(dbpassword, self.password).decode('utf8')
		sec_num = decrypt(dbpassword, self.sec_num).decode('utf8')

		accounts = {account.name:tuple(account.identifier.split('|')) for account in self.accounts}

		user = banking.SantanderUser(userID, password, sec_num, accounts)
		user.login()

		return user

	def retrieve_data(self, dbpassword, from_date, to_date):
		"""user = self.connect(dbpassword)
		data = {}
		for account in user.accounts:
			print(account.name)
			data[account.name] = {'balance': account.get_balance(), 'transactions': account.get_transactions(from_date, to_date)}
			time.sleep(5)

		print(data)"""



		for account in self.accounts:
			account.update(data[account.name])