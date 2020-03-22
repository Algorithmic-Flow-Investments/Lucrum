import os
import re
import time
from datetime import datetime, timedelta
from logging import info
from typing import Tuple, Callable, Type, Generic
from selenium import webdriver


class BankUser:
	def __init__(self):
		options = webdriver.ChromeOptions()
		# options.add_argument('headless')
		download_dir = os.path.abspath('tmp')
		preferences = {'download.default_directory': download_dir, 'directory_upgrade': True}
		options.add_experimental_option('prefs', preferences)
		self.driver = webdriver.Chrome(chrome_options=options)


class BankInterface:
	def __init__(self, name: str, identifier: Tuple, user: BankUser):
		self.name = name
		self.identifier = identifier
		self.user = user
		self.driver = self.user.driver


class BankAccount:
	def __init__(self, name: str, identifier: Tuple, user: BankUser, interface: Type[BankInterface]):
		self.name: str = name
		self.identifier = identifier
		self.user = user
		self.interface = interface(self.name, self.identifier, self.user)

	def get_transactions(self, from_date, to_date):
		statement = self.interface.get_transactions(from_date, to_date, navigate=True)
		if statement is None:
			return []
		transactions = decode_statement(statement)
		if len(transactions) < 600:
			return transactions
		else:
			transactions = []
			for date_range in date_ranges(from_date, to_date):
				statement = self.interface.get_transactions(date_range[0], date_range[1], navigate=False)
				transactions.extend(decode_statement(statement))
				time.sleep(0.5)
			return transactions

	def get_balance(self):
		return self.interface.get_balance()


def decode_statement(statement):
	transactions = []
	cur = {'date': None, 'amount': None, 'info': None}
	for line in statement.split('\n'):
		ln = line.split(': ')
		if ln[0] == 'Date':
			date = re.match(r"(\d\d/\d\d/\d\d\d\d)", ln[1]).group(0)
			cur['date'] = datetime.strptime(date, '%d/%m/%Y')
		elif ln[0] == 'Description':
			cur['info'] = ln[1].strip()
		elif ln[0] == 'Amount':
			amount = re.match(r"(\-?\d+\.\d\d)", ln[1]).group(0)
			cur['amount'] = float(amount)
			transactions.append(cur)
			cur = {'date': None, 'amount': None, 'info': None}
	return transactions


def date_ranges(min_date, max_date):
	cur_range = [min_date, min_date + timedelta(days=180)]
	ranges = []
	while True:
		if cur_range[1] > max_date:
			cur_range[1] = max_date
			ranges.append(cur_range)
			break
		ranges.append(cur_range.copy())
		cur_range[0] = cur_range[1]
		cur_range[1] += timedelta(days=180)
	return ranges


if __name__ == "__main__":
	for r in date_ranges(datetime.today() - timedelta(days=365 * 7), datetime.today()):
		print(r)
