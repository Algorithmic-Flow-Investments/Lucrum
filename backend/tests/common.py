from lucrum.app_basic import basic_app
import os


def get_context(test_func):
	app = basic_app()

	app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///" + os.path.join(os.getcwd(), 'tests/database-test.db')

	def context_wrapper():
		with app.app_context():
			test_func()

	return context_wrapper
