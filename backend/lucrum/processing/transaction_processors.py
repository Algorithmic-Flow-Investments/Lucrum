from datetime import date, datetime
from logging import warn
from typing import Optional

from dateutil.parser import parse, ParserError

from ..models import Transaction, MethodString, TargetString, Target


def process_date(transaction: Transaction):
	old_value = transaction.date
	raw = transaction.info.lower()
	if raw.find(' on ') != -1:
		split_on = raw.split(' on ')
		date_string = split_on[-1]
		date_string_split_space = date_string.split(" ", maxsplit=1)[0]
		split_date = tuple(s for s in date_string_split_space.split('-') if s != "")

		new_value: Optional[datetime] = None
		day = None
		year = None
		if len(split_date[0]) == 2:
			day = int(split_date[0])
		elif len(split_date[0]) == 4:
			year = int(split_date[0])
		else:
			warn(f"Date parsing failed (first value wrong length): {transaction.info}")
			return False

		if len(split_date) < 2:
			warn(f"Date parsing failed (date too short): {transaction.info}")
			return False
		elif len(split_date[1]) == 2:
			month = int(split_date[1])
		else:
			warn(f"Date parsing failed (month wrong length): {transaction.info}")
			return False

		if len(split_date) < 3:
			pass
		elif len(split_date[2]) == 4:
			year = int(split_date[2])
		elif len(split_date[2]) == 2:
			if day is None:
				day = int(split_date[2])

		# TODO: With these could do some shenanigans with the edges of months and years
		if year is None:
			year = transaction.data_imported.date.year
		if day is None:
			warn(f"Date parsing failed (day is None): {transaction.info}")
			return False

		new_value = datetime(year, month, day)

		if abs((new_value - transaction.data_imported.date).days) > 10:
			warn(
				f"Date parsing failed (Too far from original date): {transaction.info}, {new_value}, {transaction.data_imported.date}"
			)
			return False

		transaction.data_inferred.date = new_value
		return old_value != transaction.date
	return False


def process_method(transaction: Transaction):
	old_value = transaction.method_id
	raw = transaction.info.lower()
	for methodStr in MethodString.query.all():
		if raw.find(methodStr.string) != -1:
			transaction.data_inferred.method_id = methodStr.parent.id
			return transaction.method_id != old_value
	transaction.data_inferred.method_id = None
	return transaction.method_id != old_value


def process_target(transaction: Transaction):
	old_value = transaction.target_id

	internal, different = process_internal(transaction)
	if internal:
		return different

	raw = transaction.info.lower()
	split_ref = []
	if raw.find('ref.') != -1:
		split_ref = raw.split('ref.', maxsplit=1)
	elif raw.find('reference') != -1:
		split_ref = raw.split('reference', maxsplit=1)
	if len(split_ref) > 1:
		if split_ref[1].find('from') != -1:
			split_ref_end = split_ref[1].split('from', maxsplit=1)
		else:
			split_ref_end = split_ref[1].split(',', maxsplit=1)
		raw = split_ref[0] + split_ref_end[-1]
		transaction.data_inferred.reference = split_ref_end[0]

	for targetStr in TargetString.query.all():
		if raw.find(targetStr.string) != -1 and targetStr.parent.internal_account_id != transaction.account.target_id:
			transaction.data_inferred.target_id = targetStr.parent.id
			return transaction.target_id != old_value

	# If ignoring reference doesn't work, include it
	raw = transaction.info.lower()
	for targetStr in TargetString.query.all():
		if raw.find(targetStr.string) != -1:
			transaction.data_inferred.target_id = targetStr.parent.id
			return transaction.target_id != old_value

	transaction.data_inferred.target_id = None  # TODO: Manual clas
	return transaction.target_id != old_value


def process_internal(transaction: Transaction):
	# Finds a transaction with a complimentary amount that happens on the same day in a different account
	# and sets both transactions inferred target ids
	# TODO: maybe don't set if it already has a target?
	old_value = transaction.target_id
	mirrored_transaction: Transaction = Transaction.query.filter(Transaction.amount == -transaction.amount,
																	Transaction.date == transaction.date,
																	Transaction.account != transaction.account).first()
	if mirrored_transaction:
		this_account_target: Target = transaction.account.target
		other_account_target: Target = mirrored_transaction.account.target
		if this_account_target and other_account_target:
			mirrored_transaction.data_inferred.target_id = this_account_target.id
			transaction.data_inferred.target_id = other_account_target.id
			return True, transaction.target_id != old_value
	return False, transaction.target_id != old_value
