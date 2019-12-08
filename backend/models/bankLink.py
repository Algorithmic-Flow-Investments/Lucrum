import os
import pickle
import time
from typing import Dict, Tuple

from simplecrypt import encrypt, decrypt
from werkzeug.security import check_password_hash, generate_password_hash

import banking
from database import db


class BankLink(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	bank = db.Column(db.String(80), nullable=False)
	userID = db.Column(db.String(80), nullable=False)
	password = db.Column(db.String(80), nullable=False)
	sec_num = db.Column(db.String(80), nullable=False)
	questions = db.Column(db.BLOB, nullable=True)
	db_password_hash = db.Column(db.String(80), nullable=False)

	def __init__(self, bank, userID, password, sec_num, questions, dbpassword):
		self.bank = bank
		self.db_password_hash = generate_password_hash(dbpassword)
		self.userID = encrypt(dbpassword, userID.encode('utf8'))
		self.password = encrypt(dbpassword, password.encode('utf8'))
		self.sec_num = encrypt(dbpassword, sec_num.encode('utf8'))
		self.questions = encrypt(dbpassword, pickle.dumps(questions))

	def check_password(self, dbpassword):
		return check_password_hash(self.db_password_hash, dbpassword)

	def connect(self, dbpassword):
		if not self.check_password(dbpassword):
			return 0
		user_id: str = decrypt(dbpassword, self.userID).decode('utf8')
		password: str = decrypt(dbpassword, self.password).decode('utf8')
		sec_num: str = decrypt(dbpassword, self.sec_num).decode('utf8')
		questions: Dict[str, str] = pickle.loads(decrypt(dbpassword, self.questions))
		questions = {k.strip("?"): v for k, v in questions.items()}
		self.questions = encrypt(dbpassword, pickle.dumps(questions))
		db.session.commit()

		accounts: Dict[str, Tuple] = {account.name: tuple(account.identifier.split('|')) for account in self.accounts}

		user = banking.SantanderUser(user_id, password, sec_num, questions, accounts)
		user.login()

		return user

	def retrieve_data(self, dbpassword, from_date, to_date, force=False):
		if os.path.exists('cached.dat') and not force:
			with open('cached.dat', 'rb') as f:
				data = pickle.load(f)
		else:
			user = self.connect(dbpassword)
			data = {}
			for account in user.accounts:
				data[account.name] = {
					'balance': account.get_balance(),
					'transactions': account.get_transactions(from_date, to_date)
				}
				time.sleep(2)

			if os.path.exists('cached.dat'):
				with open('cached.dat', 'rb') as f:
					old_data = pickle.load(f)
				for k, v in data.items():
					old_data[k]['balance'] = data[k]['balance']
					old_data[k]['transactions'] = data[k]['transactions'].copy().extend(old_data[k]['transactions'])
			with open('cached.dat', 'wb') as f:
				pickle.dump(data, f)
		print(data)

		for account in self.accounts:
			account.update(data[account.name])
