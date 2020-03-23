from sqlalchemy.sql.expression import select

from lucrum.app_basic import basic_app
import os

from lucrum.database import db
from lucrum.models import Transaction


def get_context(test_func):
	app = basic_app()

	app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///" + os.path.join(os.getcwd(), 'tests/database-test.db')

	def context_wrapper():
		with app.app_context():
			test_func()

	return context_wrapper


def get_sql_value(sel, model_id, model=Transaction):
	sql_stat = select([sel]).where(model.id == model_id)
	sql_exec = db.session.get_bind().execute(sql_stat)
	fetch = sql_exec.fetchall()
	return fetch[0][0]
