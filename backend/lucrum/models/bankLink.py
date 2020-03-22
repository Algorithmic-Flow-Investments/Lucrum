import os
import pickle
import time
from datetime import datetime
from typing import Dict, Tuple, Optional

from simplecrypt import encrypt, decrypt
from werkzeug.security import check_password_hash, generate_password_hash

from ..banking import SantanderUser
from ..database import db
from .base import BaseModel


class BankLink(BaseModel):
	id = db.Column(db.Integer, primary_key=True)
	bank = db.Column(db.String(80), nullable=False)
	userID = db.Column(db.String(80), nullable=False)
	password = db.Column(db.String(80), nullable=False)
	sec_num = db.Column(db.String(80), nullable=False)
	questions = db.Column(db.BLOB, nullable=True)
	db_password_hash = db.Column(db.String(80), nullable=False)

	def __init__(self, bank, user_id, password, sec_num, questions, db_password):
		self.bank = bank
		self.db_password_hash = generate_password_hash(db_password)
		self.userID = encrypt(db_password, user_id.encode('utf8'))
		self.password = encrypt(db_password, password.encode('utf8'))
		self.sec_num = encrypt(db_password, sec_num.encode('utf8'))
		self.questions = encrypt(db_password, pickle.dumps(questions))

	def check_password(self, db_password: str) -> bool:
		return check_password_hash(self.db_password_hash, db_password)

	def connect(self, db_password: str) -> Optional[SantanderUser]:
		if not self.check_password(db_password):
			return None
		user_id: str = decrypt(db_password, self.userID).decode('utf8')
		password: str = decrypt(db_password, self.password).decode('utf8')
		sec_num: str = decrypt(db_password, self.sec_num).decode('utf8')
		questions: Dict[str, str] = pickle.loads(decrypt(db_password, self.questions))
		questions = {k.strip("?"): v for k, v in questions.items()}
		self.questions = encrypt(db_password, pickle.dumps(questions))
		db.session.commit()  # TODO: No commit in model

		accounts: Dict[str, Tuple] = {account.name: tuple(account.identifier.split('|')) for account in self.accounts}

		user = SantanderUser(user_id, password, sec_num, questions, accounts)
		user.login()

		return user

	def retrieve_data(self, db_password: str, from_date: datetime, to_date: datetime, force: bool = False) -> None:
		if os.path.exists('cached.dat') and not force:
			with open('cached.dat', 'rb') as f:
				data = pickle.load(f)
		else:
			user = self.connect(db_password)
			if user is None:
				raise Exception("Invalid login")
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
