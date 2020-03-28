from tests.common import get_context, get_sql_value
import pytest
from lucrum.database import db
from lucrum.models import Account, Transaction, Target
from datetime import datetime


@pytest.fixture(scope='function', autouse=True)
@get_context
def build_test_db():
	db.reflect()
	db.drop_all()
	db.create_all()


@get_context
def test_balance():
	acc1 = Account("Test account", "this is a test account")
	acc1.add_balance(10, datetime(2020, 1, 1))
	acc1.add_balance(15, datetime(2020, 1, 6))
	acc1.add_balance(20, datetime(2020, 1, 4))
	db.session.commit()

	assert acc1.balance == 15
	assert get_sql_value(Account.balance, acc1.id, Account) == 15


@get_context
def test_inferred_balance():
	acc1 = Account("test-santander")
	acc2 = Account("test-other")
	db.session.add_all([acc1, acc2])
	db.session.flush()

	# Test next
	# 15
	acc2.add_transaction(5, datetime(2020, 1, 7), "").data_inferred.target = acc1.target
	acc1.add_transaction(-5, datetime(2020, 1, 7), "").data_inferred.target = acc2.target
	# 10
	acc1.add_transaction(-6, datetime(2020, 1, 9), "")
	# 4
	acc2.add_transaction(-4, datetime(2020, 1, 11), "").data_inferred.target = acc1.target
	# 8
	acc1.add_transaction(2, datetime(2020, 1, 13), "")
	# 10

	# Test prev
	acc1.add_balance(10, datetime(2020, 1, 15))
	# 10
	acc1.add_transaction(-3, datetime(2020, 1, 17), "")
	# 7
	acc1.add_transaction(8, datetime(2020, 1, 19), "")
	# 15
	acc2.add_transaction(5, datetime(2020, 1, 21), "").data_inferred.target = acc1.target
	# 10
	acc1.add_transaction(5, datetime(2020, 1, 23), "")
	# 15
	acc2.add_transaction(-5, datetime(2020, 1, 25), "").data_inferred.target = acc1.target
	acc1.add_transaction(5, datetime(2020, 1, 25), "").data_inferred.target = acc2.target
	# 20
	db.session.flush()

	# Test next
	assert acc1.inferred_balance(datetime(2020, 1, 14)) == 10
	assert acc1.inferred_balance(datetime(2020, 1, 12)) == 8
	assert acc1.inferred_balance(datetime(2020, 1, 10)) == 4
	assert acc1.inferred_balance(datetime(2020, 1, 8)) == 10
	assert acc1.inferred_balance(datetime(2020, 1, 6)) == 15

	# Test prev
	assert acc1.inferred_balance(datetime(2020, 1, 16)) == 10
	assert acc1.inferred_balance(datetime(2020, 1, 18)) == 7
	assert acc1.inferred_balance(datetime(2020, 1, 20)) == 15
	assert acc1.inferred_balance(datetime(2020, 1, 22)) == 10
	assert acc1.inferred_balance(datetime(2020, 1, 24)) == 15
	assert acc1.inferred_balance(datetime(2020, 1, 26)) == 20


@get_context
def test_duplicate_import():
	acc1 = Account("test-santander")
	acc2 = Account("test-other")
	db.session.add_all([acc1, acc2])
	db.session.flush()
	t1 = acc1.add_transaction(5, datetime(2020, 1, 1), "test123")

	assert t1 is not None and t1.info == "test123"

	t2 = acc1.add_transaction(5, datetime(2020, 1, 1), "test123")

	assert t2 is None

	ts = [
		acc1.add_transaction(5, datetime(2020, 1, 1), "test1234"),
		acc1.add_transaction(6, datetime(2020, 1, 1), "test123"),
		acc1.add_transaction(5, datetime(2020, 1, 2), "test123"),
	]

	assert ts[0] is not None and ts[0].info == "test1234"
	assert ts[1] is not None and ts[1].amount == 6
	assert ts[2] is not None and ts[2].date.day == 2

	t3 = acc2.add_transaction(5, datetime(2020, 1, 1), "test123")
	assert t3 is not None and t3.info == "test123"

	now = datetime.now()

	t4 = acc1.add_transaction(5, datetime(2020, 1, 1), "abc456", now)
	t5 = acc1.add_transaction(5, datetime(2020, 1, 1), "abc456", now)
	assert t4 is not None and t5 is not None and t4.info == t5.info


@get_context
def test_internal_account():
	acc1 = Account("acc1")
	acc2 = Account("acc2")
	target1 = Target("non-acc")
	db.session.add_all([acc1, acc2, target1])
	db.session.commit()

	assert acc1.target.internal_account == acc1
	assert acc2.target.internal_account == acc2

	assert acc1.target.is_internal
	assert get_sql_value(Target.is_internal, acc1.target_id, Target)
	assert not target1.is_internal
	assert not get_sql_value(Target.is_internal, target1.id, Target)

	assert acc1.target.internal_account_id == acc1.id
	assert acc2.target.internal_account_id == acc2.id

	assert target1.internal_account_id is None

	assert Target.query.filter(Target.internal_account_id == None).first().id == target1.id


@get_context
def test_delete():
	accs = [Account("acc"), Account("acc2")]
	db.session.add_all(accs)
	db.session.commit()

	db.session.delete(accs[0])
	db.session.flush()
	assert len(Account.query.all()) == 1, "too many account"
	assert len(Target.query.all()) == 1, "too many targets"


@get_context
def plaid_fetch():
	from lucrum.models.account.account_connection import ConnectionType, AccountConnectionUser
	con_user = AccountConnectionUser(ConnectionType.PLAID, "santander",
										"access-development-c39a39dd-2bde-4084-8dc6-02a99d217f22")
	db.session.add(con_user)
	db.session.flush()
	acc1 = Account("test-santander")

	# con = acc1.add_connection(ConnectionType.PLAID, "santander", "OwkrPebEq4uaRXXQ0ZdbhBdeoomMr5H8yxvp0")

	con_user.update_balances()
	return
	db.session.flush()

	assert acc1.balance is not None and acc1.balance > 0

	transactions = con_user.update_transactions(datetime(1970, 1, 1), datetime.now())
	print(transactions)
	print(len(transactions))


if __name__ == "__main__":
	plaid_fetch()
