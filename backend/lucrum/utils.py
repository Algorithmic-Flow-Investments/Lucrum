from datetime import timedelta, date


def date_range(start_date: date, end_date: date, interval=1):
	for n in range(int((end_date - start_date).days) + 1, 0, -interval):
		yield start_date + timedelta(n)
