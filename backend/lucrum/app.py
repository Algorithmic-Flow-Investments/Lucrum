#!/usr/local/bin/python3
import logging
import sys

import flask
from flask_cors import CORS

# import server_data
from .database import db

logging.basicConfig(filename='server.log',
					format='%(asctime)s | %(filename)s:%(lineno)d | %(funcName)s | %(levelname)s | %(message)s',
					level=logging.DEBUG)
logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))


def create_app():
	app = flask.Flask(__name__)  # static_folder="../dist/assets", template_folder="../dist"
	# app.secret_key = os.urandom(24)
	CORS(app, resources={r"/api/*": {'origins': '*'}, r"/auth/*": {'origins': '*'}})

	app.config.from_pyfile('config.cfg')

	db.init_app(app)

	from .api2 import api2
	app.register_blueprint(api2)

	return app


# noinspection PyUnreachableCode
def initialise_database():
	if False: server_data.load_accounts()
	if False: server_data.new_database()
	if False: server_data.populate_database()

	server_data.prebuilt.save_all()
	server_data.db.session.commit()


if __name__ == '__main__':
	app = create_app()
	if True:
		with app.app_context():
			initialise_database()
			db.session.commit()
	app.run(debug=True, threaded=True, use_reloader=True, host='0.0.0.0')
