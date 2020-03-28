from lucrum.models import Account, Target, ScheduledTransaction
from lucrum.database import db
from datetime import datetime
import pytest

from utils import Interval
from .common import get_context


@pytest.fixture(scope='function', autouse=True)
@get_context
def build_test_db():
	db.reflect()
	db.drop_all()
	db.create_all()


@get_context
def test_monthly():
	account = Account("test-acc")

	target = Target("Bulb")

	t1 = ScheduledTransaction(account, "bills", 45, datetime(2020, 2, 3), target, Interval.MONTH)
	db.session.add(t1)
	db.session.commit()

	print(list(t1.get_occurrences(datetime(2020, 3, 1), datetime(2020, 3, 15))))


if __name__ == "__main__":
	with app.app_context():
		db.reflect()
		db.drop_all()
		db.create_all()
		test_monthly()
