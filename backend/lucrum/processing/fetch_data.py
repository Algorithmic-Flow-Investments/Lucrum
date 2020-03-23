from ..models import AccountConnectionUser
from ..database import db


def fetch_balances():
	print("FETCH DATA")
	usr: AccountConnectionUser
	for usr in AccountConnectionUser.query.all():
		usr.update_balances()
	db.session.commit()
