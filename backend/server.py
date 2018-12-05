import flask
from flask_cors import CORS

from database import db

from account import Account
from bankLink import BankLink
from transaction import *
from scheduled import ScheduledTransaction

from datetime import datetime, timedelta

from secretConfig import * # So people on Github can't see my bank details


def create_app():
	app = flask.Flask(__name__)  # static_folder="../dist/assets", template_folder="../dist"
	# app.secret_key = os.urandom(24)
	CORS(app, resources={r"/api/*": {"origins": "*"}, r"/auth/*": {"origins": "*"}})

	app.config.from_pyfile('config.cfg')
	app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

	db.init_app(app)

	from api import api
	app.register_blueprint(api)

	return app


# noinspection PyUnreachableCode
def initdb():
	if False:
		db.reflect()
		db.drop_all()
		db.create_all()

		# So people on Github can't see my bank details
		ac1 = Account(ACCOUNT1[0], ACCOUNT1[1], ACCOUNT1[2])
		ac2 = Account(ACCOUNT2[0], ACCOUNT2[1], ACCOUNT2[2])
		ac3 = Account('Limited Access Saver', description='Savings account (3%)')
		ac3.balance = 27402

		# So people on Github can't see my bank details
		bnk1 = BankLink(USER[0], USER[1], USER[2], USER[3], USER[4])

		bnk1.accounts.extend([ac1, ac2])
		db.session.add_all([bnk1, ac1, ac2, ac3, bnk1])

		tags = {
			'Parking': ['southgate shopping', 'justpark'],
			'Groceries': ['tesco storeqs'],
			'Resturaunts': ['the lime tree'],
			'Saving': ['saving'],
			'Interest': ['interest'],
			'Wages': [],
			'Loan': [],
			'Rent': []
		}

		transactionData(tags, Tag, TagString)

		methods = {
			'Card': ['card payment'],
			'Google Pay': ['via google pay'],
			'Direct Debit': ['regular transfer'],
			'Bank Transfer': ['faster payments']
		}

		transactionData(methods, Method, MethodString)

		targets = {
			'Amazon': ['amzn'],
			'JustPark': ['justpark'],
			'Tesco': ['tesco'],
			'Regular Saver': ['saving r27050318'],
			'123 Student': [],
			'Student Loans Company': [],
			'Southampton University': [],
			'Bath University': [],
			'Dominos': ['DOMINOS']
		}

		transactionData(targets, Target, TargetString)

		schedtran1 = ScheduledTransaction('Paycheck', 1707, datetime(2018, 9, 25), 'Wages', 'Bath University')
		schedtran2 = ScheduledTransaction('Loan Payment 1', 2668, datetime(2018, 9, 27), 'Loan',
											'Student Loans Company')
		schedtran3 = ScheduledTransaction('Accommodation Payment 1', -2111, datetime(2018, 10, 5), 'Rent',
											'Southampton University')
		schedtran4 = ScheduledTransaction('Regular Saver', -200, datetime(2018, 10, 1), 'Saving',
											'123 Student', monthly=True, end_date=datetime(2019, 9, 1))

		db.session.add_all([schedtran1, schedtran2, schedtran3, schedtran4])
		db.session.commit()

		#t1 = Transaction(ac1, 50, datetime(2018, 5, 31), tags=[('Groceries', 0.5), ('Parking', 0.5)], info="Test Transaction")
		#db.session.add(t1)

	bnk1 = BankLink.query.first()

	#bnk1.connect('pass123')

	bnk1.retrieve_data('pass123', datetime.today() - timedelta(days=40), datetime.today())

	db.session.commit()


def transactionData(data, dataType, dataString):
	for k, v in data.items():
		dt = dataType(k)
		db.session.add(dt)
		for st in v:
			s = dataString(dt, st)
			db.session.add(s)


if __name__ == "__main__":
	app = create_app()
	if False:
		with app.app_context():
			initdb()
	app.run(debug=True, threaded=True, use_reloader=True)
