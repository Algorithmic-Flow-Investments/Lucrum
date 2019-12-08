#!/usr/local/bin/python3
import logging

import flask
from flask_cors import CORS

from models import Account, Tag
from server_data import *

from sqlalchemy import join, select

logging.basicConfig(filename='server.log',
					format='%(asctime)s | %(filename)s:%(lineno)d | %(funcName)s | %(levelname)s | %(message)s',
					level=logging.DEBUG)
logging.getLogger().addHandler(logging.StreamHandler())


def create_app():
	app = flask.Flask(__name__)  # static_folder="../dist/assets", template_folder="../dist"
	# app.secret_key = os.urandom(24)
	CORS(app, resources={r"/api/*": {'origins': '*'}, r"/auth/*": {'origins': '*'}})

	app.config.from_pyfile('config.cfg')

	db.init_app(app)

	from api.api import api
	app.register_blueprint(api)

	return app


# noinspection PyUnreachableCode
def initialise_database():
	if False: load_accounts()
	if False: new_database()
	if False: populate_database()

	prebuilt.save_all()
	db.session.commit()
	"""transaction = Transaction(Account.query.first(), 40, datetime.today(), 'tesco')
	db.session.add(transaction)
	db.session.commit()
	t = Tag.query.filter_by(id=10).first()
	transaction.manual_tags.append(t)
	print(transaction.tags, type(transaction.tags))
	q = Tag.query.join(Transaction.tags).filter(Transaction.id == 1)
	print(q.all(), q)"""


if __name__ == '__main__':
	app = create_app()
	if True:
		with app.app_context():
			initialise_database()
	app.run(debug=True, threaded=True, use_reloader=True, host='0.0.0.0')
