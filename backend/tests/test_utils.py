from datetime import datetime

from dateutil.relativedelta import relativedelta

from lucrum.utils import date_range, Interval


def test_date_range():
	# Basic days test
	r = list(date_range(datetime(2020, 1, 1), datetime(2020, 1, 20), 3))
	assert len(r) == 7
	assert r[0] == datetime(2020, 1, 1)
	assert r[-1] == datetime(2020, 1, 19)

	r = list(date_range(datetime(2020, 1, 1), datetime(2020, 1, 20), 3, snap_end=True))
	assert len(r) == 7
	assert r[0] == datetime(2020, 1, 2)
	assert r[-1] == datetime(2020, 1, 20)

	r = list(date_range(datetime(2020, 1, 1), datetime(2020, 1, 20), 3, overflow=True))
	assert len(r) == 8
	assert r[0] == datetime(2020, 1, 1)
	assert r[-1] == datetime(2020, 1, 22)

	r = list(date_range(datetime(2020, 1, 1), datetime(2020, 1, 20), 3, snap_end=True, overflow=True))
	assert len(r) == 8
	assert r[0] == datetime(2019, 12, 30)
	assert r[-1] == datetime(2020, 1, 20)

	# Interval day test
	r = list(date_range(datetime(2020, 1, 1), datetime(2020, 1, 5), Interval.DAY))
	assert len(r) == 5
	assert r[0] == datetime(2020, 1, 1)
	assert r[-1] == datetime(2020, 1, 5)

	# Interval month test
	r = list(date_range(datetime(2019, 1, 1), datetime(2020, 2, 6), Interval.MONTH))
	print(r)
	assert len(r) == 14
	assert r[0] == datetime(2019, 1, 1)
	assert r[-1] == datetime(2020, 2, 1)

	r = list(date_range(datetime(2019, 1, 1), datetime(2020, 2, 6), Interval.MONTH, snap_end=True))
	print(r)
	assert len(r) == 14
	assert r[0] == datetime(2019, 1, 6)
	assert r[-1] == datetime(2020, 2, 6)
