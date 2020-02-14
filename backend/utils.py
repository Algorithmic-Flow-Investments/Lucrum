from datetime import timedelta, datetime


def date_range(start_date: datetime, end_date: datetime, interval=1):
	for n in range(int((end_date - start_date).days) + 1, 0, -interval):
		yield start_date + timedelta(n)
