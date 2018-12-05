import urllib.parse
from datetime import timedelta

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
import qifparse

import os

from ..common import BankAccount

class SantanderUser():
	def __init__(self, userID, password, secNum, accounts={}):
		"""

		:param userID:
		:param password:
		:param secNum:
		:param accounts: A dict of identifier:name
		"""
		self.userID = userID
		self.password = password
		self.secNum = secNum
		options = webdriver.ChromeOptions()
		#options.add_argument('headless')
		download_dir = os.path.abspath("tmp")
		preferences = {"download.default_directory": download_dir,
		               "directory_upgrade": True}
		options.add_experimental_option("prefs", preferences)
		self.driver = webdriver.Chrome(chrome_options=options)
		self.accounts = []
		for name, identifier in accounts.items():
			self.accounts.append(SantanderAccount(name, identifier, self))

	def screenshot(self):
		self.driver.get_screenshot_as_file('screenshot.png')

	def login(self):
		driver = self.driver

		driver.get('https://retail.santander.co.uk/LOGSUK_NS_ENS/BtoChannelDriver.ssobto?dse_operationName=LOGON&dse_processorState=initial&redirect=S')

		driver.implicitly_wait(3)
		elem = driver.find_element_by_id('infoLDAP_E.customerID')
		elem.send_keys(self.userID)
		elem.send_keys(Keys.RETURN)

		try:
			challenge = driver.find_element_by_css_selector('[id="cbQuestionChallenge.responseUser"]')
			question = driver.find_element_by_css_selector('form .form-item .data').text.strip()
			answer = input("Verifying new computer:\n\t{}? ".format(question))
			challenge.send_keys(answer)
			challenge.send_keys(Keys.RETURN)
		except NoSuchElementException as e:
			print("Verification not needed?")

		try:
			phrase = driver.find_element_by_css_selector('.imgSection span')
			print(phrase.text.strip())
		except NoSuchElementException:
			print("No magic phrase")


		# login
		for i in range(1, len(self.password) + 1):
			try:
				password = driver.find_element_by_id('signPosition' + str(i))
			except NoSuchElementException:
				pass
			else:
				password.send_keys(self.password[i - 1])

		for i in range(1, len(self.secNum) + 1):
			try:
				secNum = driver.find_element_by_id('passwordPosition' + str(i))
			except NoSuchElementException:
				pass
			else:
				secNum.send_keys(self.secNum[i - 1])

		password.send_keys(Keys.RETURN)

		driver.implicitly_wait(1)

		try:
			driver.find_element_by_class_name('submit').click()
		except NoSuchElementException:
			pass
	def go_home(self):
		self.driver.get('https://retail.santander.co.uk/EBAN_Accounts_ENS/channel.ssobto?dse_operationName=MyAccounts')

class SantanderAccount(BankAccount):
	def __init__(self, name, identifier, user):
		super().__init__(name, identifier, user)

	def goto_page(self):
		self.user.go_home()
		driver = self.driver
		accounts = (driver
		            .find_element_by_css_selector('.accountlist')
		            .find_elements_by_css_selector('li .info')
		            )
		account_map = {
			tuple(acc.find_element_by_css_selector('.number').text.split(' ')): acc
			for acc in accounts
		}

		# choose our account
		acc = account_map[self.identifier]
		acc.find_element_by_css_selector('a').click()

	def get_balance(self):
		self.user.go_home()
		driver = self.driver
		accounts = (driver
		            .find_element_by_css_selector('.accountlist')
		            .find_elements_by_css_selector('li .info')
		            )
		account_map = {
			tuple(acc.find_element_by_css_selector('.number').text.split(' ')): acc
			for acc in accounts
		}

		# choose our account
		acc = account_map[self.identifier]

		accp = acc.find_element_by_xpath('..')

		amount = accp.find_element_by_class_name('amount').get_attribute('innerHTML')

		return float(amount.replace('£', '').replace(',', ''))

	def get_transactions(self, from_date, to_date):
		self.goto_page()
		driver = self.driver

		# upper bound is inclusive for santander
		to_date_incl = to_date - timedelta(days=1)

		download_link = WebDriverWait(driver, 10).until(
	        EC.presence_of_element_located((By.CSS_SELECTOR, ".download"))
	    )
		download_link.click()

		Select(driver.find_element_by_css_selector('#sel_downloadto')).select_by_visible_text('Intuit Quicken (QIF)')


		from_day = driver.find_element_by_css_selector('[name="downloadStatementsForm.fromDate.day"]')
		from_month = driver.find_element_by_css_selector('[name="downloadStatementsForm.fromDate.month"]')
		from_year = driver.find_element_by_css_selector('[name="downloadStatementsForm.fromDate.year"]')

		from_day.clear()
		from_day.send_keys(str(from_date.day))
		from_month.clear()
		from_month.send_keys(str(from_date.month))
		from_year.clear()
		from_year.send_keys(str(from_date.year))


		to_day = driver.find_element_by_css_selector('[name="downloadStatementsForm.toDate.day"]')
		to_month = driver.find_element_by_css_selector('[name="downloadStatementsForm.toDate.month"]')
		to_year = driver.find_element_by_css_selector('[name="downloadStatementsForm.toDate.year"]')

		to_day.clear()
		to_day.send_keys(str(to_date_incl.day))
		to_month.clear()
		to_month.send_keys(str(to_date_incl.month))
		to_year.clear()
		to_year.send_keys(str(to_date_incl.year))

		try:
			driver.find_element_by_css_selector('close').click()
		except NoSuchElementException:
			pass

		driver.find_element_by_css_selector('[name="downloadStatementsForm.events.0"]').click()

		return super().get_transactions()