import os
import re
from datetime import datetime, timedelta
from typing import List, Union, Dict

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.select import Select

from lucrum.utils import date_ranges
from .generic import Scraper
from time import sleep


class Santander(Scraper):
	def __init__(self, token: dict):
		super().__init__(token)
		self.personal_id = token['personal_id']
		self.password = token['password']
		self.security_number = token['security_number']
		self.questions = token['questions']

	def login(self):
		driver = self.driver

		driver.get("https://retail.santander.co.uk/olb/app/logon/access/#/logon")

		driver.implicitly_wait(1)

		# Close the box that says "we'll never call you and ask to log on"
		got_it = driver.find_element_by_id('gotItbtn')
		got_it.click()

		# Enter personal id
		pid = driver.find_element_by_id('pid')
		pid.send_keys(self.personal_id)

		# Enter security number
		sec = driver.find_element_by_id('securityNumber')
		sec.send_keys(self.security_number)

		# Press log in button
		login = driver.find_element_by_id('submitbtn')
		login.click()

		try:
			send_code = driver.find_element_by_id('sendcode')
			send_code.click()

			code_entry = driver.find_element_by_id('pwd')
			otp = input("Enter OTP:")  # TODO: Replace with proper frontend solution
			code_entry.send_keys(otp)

			submit = driver.find_element_by_id('btnsubmit')
			submit.click()
		except NoSuchElementException:
			pass

		for i in range(10):
			if 'Important service message' in driver.page_source:
				primary = driver.find_element_by_name('buttonsInterstitial.events.1')
				primary.click()
				print("Important message")
				break
			if 'My accounts' in driver.page_source:
				print("Logged in!")
				break
			sleep(0.5)
		sleep(1)

	def go_home(self):
		self.driver.get('https://retail.santander.co.uk/EBAN_Accounts_ENS/channel.ssobto?dse_operationName=MyAccounts')

	def get_balance(self, identifier: str) -> float:
		driver = self.driver

		# Go to the accounts page
		self.go_home()
		accounts = (driver.find_element_by_css_selector('.accountlist').find_elements_by_css_selector('li .info'))
		account_map = {acc.find_element_by_css_selector('.number').text: acc for acc in accounts}

		# choose our account
		acc = account_map[identifier]
		accp = acc.find_element_by_xpath('..')
		amount = accp.find_element_by_class_name('amount').get_attribute('innerHTML')

		return float(amount.replace('£', '').replace(',', ''))

	def get_transactions(self, identifier: str, start_date: datetime, end_date: datetime) -> List[dict]:
		lowest_date = datetime.today() - timedelta(days=365 * 7)
		if start_date < lowest_date:
			start_date = lowest_date
		driver = self.driver

		# upper bound is inclusive for Santander
		end_date_incl = end_date  # - timedelta(days=1)

		# Go to the accounts page
		self.go_home()
		accounts = (driver.find_element_by_css_selector('.accountlist').find_elements_by_css_selector('li .info'))
		account_map = {acc.find_element_by_css_selector('.number').text: acc for acc in accounts}

		# choose our account
		acc = account_map[identifier]
		acc.find_element_by_css_selector('a').click()

		download_link = driver.find_element_by_css_selector('.download')
		download_link.click()

		Select(driver.find_element_by_css_selector('#sel_downloadto')).select_by_visible_text('Text file (TXT)')

		super().pre_download()

		return self._download_transactions(start_date, end_date_incl)

	def _download_transactions(self, start_date: datetime, end_date: datetime, level: int = 1) -> List[dict]:
		driver = self.driver

		driver.implicitly_wait(3)

		from_day = driver.find_element_by_css_selector('[name="downloadStatementsForm.fromDate.day"]')
		from_month = driver.find_element_by_css_selector('[name="downloadStatementsForm.fromDate.month"]')
		from_year = driver.find_element_by_css_selector('[name="downloadStatementsForm.fromDate.year"]')

		from_day.clear()
		from_day.send_keys(str(start_date.day))
		from_month.clear()
		from_month.send_keys(str(start_date.month))
		from_year.clear()
		from_year.send_keys(str(start_date.year))

		to_day = driver.find_element_by_css_selector('[name="downloadStatementsForm.toDate.day"]')
		to_month = driver.find_element_by_css_selector('[name="downloadStatementsForm.toDate.month"]')
		to_year = driver.find_element_by_css_selector('[name="downloadStatementsForm.toDate.year"]')

		to_day.clear()
		to_day.send_keys(str(end_date.day))
		to_month.clear()
		to_month.send_keys(str(end_date.month))
		to_year.clear()
		to_year.send_keys(str(end_date.year))

		driver.implicitly_wait(1)

		try:
			driver.find_element_by_css_selector('close').click()
		except NoSuchElementException:
			pass

		driver.implicitly_wait(3)

		driver.find_element_by_css_selector('[name="downloadStatementsForm.events.0"]').click()

		while len(os.listdir('tmp')) == 0 or os.listdir('tmp')[0][-3:] != 'txt':
			sleep(0.1)
			if len(self.driver.find_elements_by_link_text('Back to My accounts')) > 0:
				return []
		file_name = 'tmp/' + os.listdir('tmp')[0]
		print('file', file_name)

		with open(file_name, 'r', encoding='ISO-8859-1') as f:
			contents = f.read()

		os.remove(file_name)

		transactions = self.decode_statement(contents)

		if len(transactions) < 600:
			return transactions
		else:
			transactions = []
			for date_range in date_ranges(start_date, end_date, 180 / level):
				new_transactions = self._download_transactions(date_range[0], date_range[1], level=level + 1)
				transactions.extend(new_transactions)
				sleep(0.5)
			return transactions

	@staticmethod
	def decode_statement(statement) -> List[dict]:
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
				amount = re.match(r"(-?\d+\.\d\d)", ln[1]).group(0)
				cur['amount'] = float(amount)
				transactions.append(cur.copy())
				cur = {'date': None, 'amount': None, 'info': None}
		return transactions
