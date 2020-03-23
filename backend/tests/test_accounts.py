from .common import get_context, get_sql_value
import pytest
from lucrum.database import db
from lucrum.models import Account, Transaction
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
	db.session.flush()

	assert acc1.balance == 15
	assert get_sql_value(Account.balance, acc1.id, Account) == 15


@get_context
def test_inferred_balance():
	acc1 = Account("test-santander")
	acc2 = Account("test-other")
	db.session.add_all([acc1, acc2])
	db.session.flush()
	t1 = acc1.add_transaction(8, datetime(2020, 1, 3), "")
	t1.set_target(acc2.target)
	t2 = acc1.add_transaction(-3, datetime(2020, 1, 7), "")
	t2.set_target(acc2.target)
	db.session.commit()

	assert acc2.inferred_balance(datetime(2020, 1, 6)) == -8
	assert acc2.inferred_balance(datetime(2020, 1, 8)) == -5

	# 15
	t3 = acc2.add_transaction(5, datetime(2020, 1, 2), "")
	t3.set_target(acc1.target)
	# 10
	acc1.add_balance(10, datetime(2020, 1, 4))
	# 10
	t4 = acc2.add_transaction(-5, datetime(2020, 1, 6), "")
	t4.set_target(acc1.target)
	# 15
	t5 = acc2.add_transaction(-5, datetime(2020, 1, 8), "")
	t5.set_target(acc1.target)
	# 20
	acc1.add_balance(20, datetime(2020, 1, 10))
	# 20
	t6 = acc2.add_transaction(-5, datetime(2020, 1, 12), "")
	t6.set_target(acc1.target)
	# 25

	assert acc1.inferred_balance(datetime(2020, 1, 1)) == 15
	assert acc1.inferred_balance(datetime(2020, 1, 3)) == 10
	assert acc1.inferred_balance(datetime(2020, 1, 5)) == 10
	assert acc1.inferred_balance(datetime(2020, 1, 7)) == 15
	assert acc1.inferred_balance(datetime(2020, 1, 9)) == 20
	assert acc1.inferred_balance(datetime(2020, 1, 11)) == 20
	assert acc1.inferred_balance(datetime(2020, 1, 13)) == 25


@get_context
def plaid_fetch():
	from lucrum.models.account.account_connection import ConnectionType, AccountConnectionUser
	con_user = AccountConnectionUser(ConnectionType.PLAID, "santander",
										"access-development-c39a39dd-2bde-4084-8dc6-02a99d217f22")
	db.session.add(con_user)
	db.session.flush()
	acc1 = Account("test-santander")

	con = acc1.add_connection(ConnectionType.PLAID, "santander", "OwkrPebEq4uaRXXQ0ZdbhBdeoomMr5H8yxvp0")

	con_user.update_balances()
	db.session.flush()

	assert acc1.balance is not None and acc1.balance > 0

	transactions = con_user.update_transactions(datetime(1970, 1, 1), datetime.now())
	print(transactions)
	print(len(transactions))
