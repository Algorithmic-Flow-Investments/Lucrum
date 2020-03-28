from sqlalchemy import select, text, table
from werkzeug.datastructures import MultiDict

from lucrum.models import Account, Transaction, Target, TargetString, MethodString, Method, Tag, TransactionImported, \
 TransactionInferred, TransactionManual
from lucrum.database import db
from datetime import datetime
from lucrum.api import transactions, meta
import pytest

from lucrum.processing.transaction_processors import process_internal
from .common import get_context, get_sql_value

from lucrum.processing import transaction_processors


@pytest.fixture(scope='function', autouse=True)
@get_context
def build_test_db():
	db.reflect()
	db.drop_all()
	db.create_all()


@get_context
def test_date():
	account = Account("test-acc")

	t1 = Transaction(account, 5, datetime(2020, 2, 3))
	t1.process()
	db.session.add(t1)
	db.session.commit()

	assert t1.date == datetime(2020, 2, 3)
	assert get_sql_value(Transaction.date, t1.id) == datetime(2020, 2, 3)

	t1.data_imported.info = "CARD PAYMENT TO SAINSBURYS S/MKTS,7.35 GBP, RATE 1.00/GBP ON 31-01-2020"
	transaction_processors.process_date(t1)
	db.session.commit()
	assert t1.date == datetime(2020, 1, 31)
	assert get_sql_value(Transaction.date, t1.id) == datetime(2020, 1, 31)

	t1.data_imported.info = "CARD PAYMENT TO SAINSBURYS S/MKTS,7.35 GBP, RATE 1.00/GBP ON 31-01-202"
	t1.data_inferred.date = None
	transaction_processors.process_date(t1)
	assert t1.date == datetime(2020, 1, 31)

	t1.data_imported.info = "CARD PAYMENT TO SAINSBURYS S/MKTS,7.35 GBP, RATE 1.00/GBP ON 31-01-20"
	t1.data_inferred.date = None
	transaction_processors.process_date(t1)
	assert t1.date == datetime(2020, 1, 31)

	t1.data_imported.info = "CARD PAYMENT TO SAINSBURYS S/MKTS,7.35 GBP, RATE 1.00/GBP ON 31-01-2"
	t1.data_inferred.date = None
	transaction_processors.process_date(t1)
	assert t1.date == datetime(2020, 1, 31)

	t1.data_imported.info = "CARD PAYMENT TO SAINSBURYS S/MKTS,7.35 GBP, RATE 1.00/GBP ON 31-01-"
	t1.data_inferred.date = None
	transaction_processors.process_date(t1)
	assert t1.date == datetime(2020, 1, 31)

	t1.data_imported.info = "CARD PAYMENT TO SAINSBURYS S/MKTS,7.35 GBP, RATE 1.00/GBP ON 31-01"
	t1.data_inferred.date = None
	transaction_processors.process_date(t1)
	assert t1.date == datetime(2020, 1, 31)

	t1.data_imported.info = "CARD PAYMENT TO SAINSBURYS S/MKTS,7.35 GBP, RATE 1.00/GBP ON 2020-01-31"
	t1.data_inferred.date = None
	transaction_processors.process_date(t1)
	assert t1.date == datetime(2020, 1, 31)

	t1.data_manual.date = datetime(2020, 4, 3)
	db.session.commit()
	assert t1.date == datetime(2020, 4, 3)
	assert get_sql_value(Transaction.date, t1.id) == datetime(2020, 4, 3)


@get_context
def test_target():
	account = Account("test-acc")
	db.session.flush()
	target1 = Target("Sains-test")
	ts = TargetString(target1, "sainsburys")
	db.session.add_all([account, target1])
	db.session.flush()

	t1 = Transaction(account, 5, datetime(2020, 2, 3),
						"CARD PAYMENT TO SAINSBURYS S/MKTS,7.35 GBP, RATE 1.00/GBP ON 31-01-2020")
	t1.process()
	db.session.add(t1)
	db.session.commit()

	assert t1.target_id == target1.id, "target_id not correct"
	assert t1.target.id == target1.id, "target.id not correct"
	assert get_sql_value(Transaction.target_id, t1.id) == target1.id, "SQL target ID not correct"
	assert len(target1.transactions) == 1, "Target has too many transactions"

	target2 = Target("Sains-test-two")
	db.session.add(target2)
	db.session.commit()
	t1.data_manual.target_id = target2.id
	db.session.commit()

	assert t1.target_id == target2.id
	assert t1.target.id == target2.id
	assert get_sql_value(Transaction.target_id, t1.id) == target2.id


@get_context
def test_internal_target():
	acc1 = Account("test-acc-one")
	acc2 = Account("test-acc-two")
	db.session.add_all([acc1, acc2])
	db.session.commit()

	t1 = Transaction(acc1, 5, datetime(2020, 1, 5))
	# t1.data_inferred.target = acc2.target
	t2 = Transaction(acc2, -5, datetime(2020, 1, 5))
	# t2.data_inferred.target = acc1.target
	t3 = Transaction(acc1, 8, datetime(2020, 4, 5))
	db.session.add_all([t1, t2, t3])
	process_internal(t1)
	process_internal(t2)
	assert t1.target_id == acc2.target.id
	assert t2.target_id == acc1.target.id

	assert t1.mirrored_transaction == t2
	assert t2.mirrored_transaction == t1


@get_context
def test_method():
	account = Account("test-acc")

	method1 = Method("Card payment test")
	db.session.add(method1)
	ms = MethodString(method1, "card payment")
	db.session.add(ms)

	t1 = Transaction(account, 5, datetime(2020, 2, 3),
						"CARD PAYMENT TO SAINSBURYS S/MKTS,7.35 GBP, RATE 1.00/GBP ON 31-01-2020")
	t1.process()
	db.session.add(t1)
	db.session.commit()

	assert t1.method_id == method1.id
	assert t1.method.id == method1.id
	assert get_sql_value(Transaction.method_id, t1.id) == method1.id

	method2 = Method("Card payment test two")
	db.session.add(method2)
	db.session.commit()
	t1.data_manual.method_id = method2.id
	db.session.commit()

	assert t1.method_id == method2.id
	assert t1.method.id == method2.id
	assert get_sql_value(Transaction.method_id, t1.id) == method2.id


@get_context
def test_amount():
	account = Account("test-acc")
	db.session.add(account)
	db.session.flush()
	t1 = Transaction(account, 5, datetime(2020, 2, 3),
						"CARD PAYMENT TO SAINSBURYS S/MKTS,7.35 GBP, RATE 1.00/GBP ON 31-01-2020")
	t1.process()
	db.session.add(t1)
	db.session.commit()
	assert t1.amount == 5
	assert get_sql_value(Transaction.amount, t1.id) == 5

	t1.data_manual.amount = 10
	db.session.commit()
	assert t1.amount == 10
	assert get_sql_value(Transaction.amount, t1.id) == 10


@get_context
def test_tags():
	account = Account("test-acc")
	target1 = Target("Sains-test")
	ts = TargetString(target1, "sainsburys")
	tag1 = Tag("tag1")
	target1.tags.append(tag1)

	db.session.add_all([account, target1])
	db.session.flush()
	t1 = Transaction(account, 5, datetime(2020, 2, 3),
						"CARD PAYMENT TO SAINSBURYS S/MKTS,7.35 GBP, RATE 1.00/GBP ON 31-01-2020")
	t1.process()
	db.session.add(t1)

	t2 = Transaction(account, 8, datetime(2020, 2, 4), None)
	tagB = Tag("tagB")
	t2.data_manual.tags.append(tagB)
	db.session.add(t2)
	db.session.commit()

	assert t1.data_inferred.tags[0]
	assert t1.data_inferred.tags[0].id == tag1.id and len(t1.data_inferred.tags) == 1
	assert t1.tags[0].id == tag1.id and len(t1.tags) == 1

	tagA = Tag("tagA")
	t1.data_manual.tags.append(tagA)
	db.session.commit()

	assert t1.data_manual.tags[0]
	assert t1.data_manual.tags[0].id == tagA.id and len(t1.data_manual.tags) == 1
	assert t1.tags[0].id == tag1.id and t1.tags[1].id == tagA.id and len(t1.tags) == 2

	target2 = Target("Sains-test-two")
	tag2 = Tag("tag2")
	target2.tags.append(tag2)
	db.session.add(target2)
	db.session.commit()
	t1.data_manual.target_id = target2.id
	db.session.commit()

	assert t1.tags[1].id == tag2.id and t1.tags[0].id == tagA.id and len(t1.tags) == 2

	q = Tag.query.join(Transaction.tags).all()

	assert [t.id for t in q] == [3, 4, 2]


@get_context
def test_api():
	account = Account("test-acc")
	account2 = Account("test-bank")
	db.session.add_all([account, account2])
	db.session.flush()
	target1 = Target("Sains-test")
	ts = TargetString(target1, "sainsburys")
	tag1 = Tag("tag1")
	target1.tags.append(tag1)
	db.session.add(target1)

	ts2 = TargetString(account2.target, "bank")

	t1 = Transaction(account, 5, datetime(2020, 2, 3), "CARD PAYMENT TO bank,7.35 GBP, RATE 1.00/GBP ON 31-01-2020")
	t1.process()
	db.session.add(t1)

	t2 = Transaction(account, 8, datetime(2020, 2, 3),
						"CARD PAYMENT TO SAINSBURYS S/MKTS,7.35 GBP, RATE 1.00/GBP ON 31-01-2020")
	t2.process()
	db.session.add(t2)

	db.session.commit()

	query = MultiDict([
		('min', '2020-02-02'),
		('max', '2020-02-04'),
	])

	lst = transactions.transactions_list(query)
	assert [t['id'] for t in lst] == [1, 2]

	stats = transactions.stats(query)
	assert stats['total']['gross'] == 8

	mstats = meta.stats(None)
	assert mstats['transactions'] == 2


@get_context
def test_deletion():
	account = Account("test-acc")
	target = Target("test-target")
	tag = Tag("test-tag")
	target.tags.append(tag)
	db.session.add_all([account, target, tag])
	db.session.flush()
	ts = [
		Transaction(account, t, datetime(2020, 2, 3), "CARD PAYMENT TO bank,7.35 GBP, RATE 1.00/GBP ON 31-01-2020")
		for t in range(5)
	]
	ts[0].data_inferred.target = target
	db.session.add_all(ts)
	db.session.commit()

	def _check_all(expected):
		assert [t.id for t in Transaction.query.all()] == expected
		assert [t.id for t in TransactionImported.query.all()] == expected
		assert [t.id for t in TransactionInferred.query.all()] == expected
		assert [t.id for t in TransactionManual.query.all()] == expected

	_check_all([1, 2, 3, 4, 5])

	# print(ts[0].data_inferred.target.tags)

	db.session.delete(Transaction.query.first())
	db.session.commit()

	_check_all([2, 3, 4, 5])

	Transaction.query.filter(Transaction.id == 2).delete()
	db.session.commit()

	_check_all([3, 4, 5])

	db.session.delete(TransactionInferred.query.first())
	db.session.commit()

	for t in Transaction.query.all():
		db.session.delete(t)
	_check_all([])
