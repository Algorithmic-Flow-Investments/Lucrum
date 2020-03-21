from datetime import date, datetime

from dateutil.parser import parse, ParserError

from models import Transaction, MethodString, TargetString, Target


def process_date(transaction: Transaction):
	old_value = transaction.date
	raw = transaction.info.lower()
	if raw.find(' on ') != -1:
		split_on = raw.split(' on ')
		date_string = split_on[-1]
		date_string_split_space = date_string.split(" ", maxsplit=1)[0]
		split_day_month = [s for s in date_string_split_space.split('-') if s != ""]
		try:
			if len(split_day_month[0]) == 4:
				new_value = parse(date_string_split_space)
			else:
				new_value = parse(date_string_split_space, dayfirst=True)
		except ParserError:
			if len(split_day_month) == 2:
				new_value = datetime(transaction.date.year, int(split_day_month[1]), int(split_day_month[0]))
			else:
				print("FAILED", raw)
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
	split = []
	if raw.find('ref.') != -1:
		split = raw.split('ref.', maxsplit=1)
	elif raw.find('reference') != -1:
		split = raw.split('reference', maxsplit=1)
	if len(split) > 1:
		if split[1].find('from') != -1:
			split2 = split[1].split('from', maxsplit=1)
		else:
			split2 = split[1].split(',', maxsplit=1)
		raw = split[0] + split2[-1]
		transaction.data_inferred.reference = split2[0]

	for targetStr in TargetString.query.all():
		if raw.find(targetStr.string) != -1:
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
	old_value = transaction.target_id
	mirrored_transaction: Transaction = Transaction.query.filter(Transaction.amount == -transaction.amount,
																	Transaction.date == transaction.date,
																	Transaction.account != transaction.account).first()
	if mirrored_transaction:
		this_account_target: Target = Target.query.filter(Target.name == transaction.account.name).first()
		other_account_target: Target = Target.query.filter(Target.name == mirrored_transaction.account.name).first()
		if this_account_target and other_account_target:
			mirrored_transaction.data_inferred.target_id = this_account_target.id
			transaction.data_inferred.target_id = other_account_target.id
			return True, transaction.target_id != old_value
	return False, transaction.target_id != old_value
