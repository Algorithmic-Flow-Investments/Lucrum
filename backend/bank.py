import banking
from datetime import datetime, timedelta
import os
from qifparse.parser import QifParser


def get_data():
	accounts = {'123 Student':('09-01-28', '01213822'), 'Regular Saver': ('SAVING', 'R27050318', 'WAT')}
	a = banking.SantanderUser('', '', '', accounts)
	a.login()
	a.accounts[0].goto_page()
	a.accounts[0].get_transactions(datetime.today() - timedelta(days=7), datetime.today())

if __name__ == "__main__":
	#get_data()
	#for file in os.listdir('tmp'):
	#	qif = QifParser.parse(file('tmp/' + file))
	banking.decodeQif()