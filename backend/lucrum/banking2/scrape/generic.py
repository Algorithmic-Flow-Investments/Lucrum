import abc
import os
from datetime import datetime
from typing import List

from selenium import webdriver


class Scraper:
	def __init__(self, token: dict):
		self.token = token
		options = webdriver.ChromeOptions()
		# options.add_argument('headless')
		download_dir = os.path.abspath('tmp')
		preferences = {'download.default_directory': download_dir, 'directory_upgrade': True}
		options.add_experimental_option('prefs', preferences)
		self.driver = webdriver.Chrome(chrome_options=options)

	@abc.abstractmethod
	def login(self):
		pass

	@abc.abstractmethod
	def get_balance(self, identifier: str) -> float:
		pass

	@abc.abstractmethod
	def get_transactions(self, identifier: str, start_date: datetime, end_date: datetime) -> List[dict]:
		pass

	def pre_download(self):
		if not os.path.exists('tmp'):
			os.mkdir('tmp')
		else:
			for filename in os.listdir('tmp'):
				file_path = os.path.join('tmp', filename)
				os.remove(file_path)
