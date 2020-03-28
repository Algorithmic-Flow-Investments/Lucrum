import enum
from datetime import timedelta, date, datetime
from typing import Union, Generator

from dateutil.relativedelta import relativedelta


class Interval(enum.Enum):
	DAY = 1
	WEEK = 7
	FORTNIGHT = 14
	MONTH = 30
	YEAR = 365


def relative_delta_to_months(delta: relativedelta):
	return delta.years * 12 + delta.months


def date_range(start_date: datetime,
				end_date: datetime,
				interval: Union[Interval, int] = 1,
				snap_end=False,
				overflow=False) -> Generator[Union[datetime], None, None]:
	"""

	:param start_date: The start (earliest) date
	:param end_date: The end (latest) date
	:param interval: The Interval between dates in the sequence. Can be an int or an Interval
	:param snap_end: If true the sequence will be snapped to the end date rather than the start date
	:param overflow: Should the sequence overflow its bounds if it doesn't fit neatly within the dates?
	"""
	count = 0
	change = 0
	if interval == Interval.DAY:
		interval = 1
	elif interval == Interval.WEEK:
		# TODO: Possibly add option to snap to interval
		interval = 7
	elif interval == Interval.FORTNIGHT:
		interval = 14
	elif interval == Interval.MONTH:
		diff = relativedelta(end_date, start_date)
		count = relative_delta_to_months(diff)
		change = relativedelta(months=1)
	if type(interval) == int:
		diff = (end_date - start_date)
		count = diff.days // interval
		if diff.days % interval != 0 and overflow:
			count += 1
		change = relativedelta(days=interval)
	if not snap_end:
		for n in range(0, count + 1, 1):
			yield start_date + change * n
	else:
		for n in range(count, -1, -1):
			yield end_date - change * n


def date_ranges(min_date, max_date, interval=180):
	cur_range = [min_date, min_date + timedelta(days=interval)]
	ranges = []
	while True:
		if cur_range[1] > max_date:
			cur_range[1] = max_date
			ranges.append(cur_range)
			break
		ranges.append(cur_range.copy())
		cur_range[0] = cur_range[1] + timedelta(days=1)
		cur_range[1] += timedelta(days=interval)
	return ranges


if __name__ == "__main__":
	print(date_ranges(date(2013, 1, 1), date(2020, 3, 11)))
