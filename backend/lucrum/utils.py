from datetime import timedelta, date


def date_range(start_date: date, end_date: date, interval=1):
	for n in range(int((end_date - start_date).days) + 1, 0, -interval):
		yield start_date + timedelta(n)


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
