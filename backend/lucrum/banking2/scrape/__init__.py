from .santander import Santander


def new_scraper(bank, token):
	if bank == "santander":
		return Santander(token)
