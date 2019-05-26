import flask
from flask_cors import CORS

from models import *

from datetime import datetime, timedelta

from secretConfig import *  # So people on Github can't see my bank details

import prebuilt

from sqlalchemy import join


def create_app():
	app = flask.Flask(__name__)  # static_folder="../dist/assets", template_folder="../dist"
	# app.secret_key = os.urandom(24)
	CORS(app, resources={r"/api/*": {"origins": "*"}, r"/auth/*": {"origins": "*"}})

	app.config.from_pyfile('config.cfg')
	app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

	db.init_app(app)

	from api.api import api
	app.register_blueprint(api)

	return app


# noinspection PyUnreachableCode
def initdb():
	if False:
		db.reflect()
		print("Dropping...")
		db.drop_all()
		print("Created...")
		db.create_all()
		print("Populating...")

		# So people on Github can't see my bank details
		ac1 = Account(ACCOUNT1[0], ACCOUNT1[1], ACCOUNT1[2])
		ac2 = Account(ACCOUNT2[0], ACCOUNT2[1], ACCOUNT2[2])
		ac3 = Account(ACCOUNT3[0], ACCOUNT3[1], ACCOUNT3[2])

		# So people on Github can't see my bank details
		bnk1 = BankLink(USER[0], USER[1], USER[2], USER[3], USER[4], USER[5])

		bnk1.accounts.extend([ac1, ac2, ac3])
		db.session.add_all([bnk1, ac1, ac2, ac3])

		methods = prebuilt.METHODS

		transactionData(methods, Method, MethodString)

		targets = prebuilt.TARGETS

		transactionData(targets, Target, TargetString)

		tags = prebuilt.TAGS

		transactionData(tags, Tag, None)

		schedtran1 = ScheduledTransaction('Paycheck', 1707, datetime(2018, 9, 25), 'Wages', 'Bath University')
		schedtran2 = ScheduledTransaction('Loan Payment 1', 2668, datetime(2018, 9, 27), 'Loan',
											'Student Loans Company')
		schedtran3 = ScheduledTransaction('Accommodation Payment 1', -2111, datetime(2018, 10, 5), 'Rent',
											'Southampton University')
		schedtran4 = ScheduledTransaction('Regular Saver', -200, datetime(2018, 10, 1), 'Saving',
											'123 Student', monthly=True, end_date=datetime(2019, 9, 1))

		db.session.add_all([schedtran1, schedtran2, schedtran3, schedtran4])
		db.session.commit()
		print("Done!\n\n")

		#t1 = Transaction(ac1, 50, datetime(2018, 5, 31), tags=[('Groceries', 0.5), ('Parking', 0.5)], info="Test Transaction")
		#db.session.add(t1)

	bnk1 = BankLink.query.first()

	#bnk1.connect('pass123')

	bnk1.retrieve_data('pass123', datetime.today() - timedelta(days=365), datetime.today())

	db.session.commit()

	prebuilt.save_all()

	print("== 1 ==")
	t = Transaction.query.filter(Transaction.id == 1).first()  # type: Transaction
	print(t.tags)
	print(t.exclude)

	print("== 3 ==")
	t = Transaction.query.filter(Transaction.id == 3).first()  # type: Transaction
	print(t.tags)
	print(t.exclude)

def transactionData(data, dataType, dataString):
	for name, data in data.items():
		data_object = dataType.query.filter_by(name=name).first()
		if data_object is None:
			data_object = dataType(name)
		db.session.add(data_object)
		if dataString is None:
			for target_name in data[0]:
				t = Target.query.filter_by(name=target_name).first()
				if t is not None:
					data_object.targets.append(t)
			data_object.exclude = data[1]
		else:
			for data_string in data:
				s = dataString(data_object, data_string)
				db.session.add(s)


if __name__ == "__main__":
	app = create_app()
	if True:
		with app.app_context():
			initdb()
	app.run(debug=True, threaded=True, use_reloader=True, host='0.0.0.0')
