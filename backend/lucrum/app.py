#!/usr/local/bin/python3
import logging
import os
import sys

import flask
from flask_cors import CORS

# import server_data
from lucrum.database import db

logging.basicConfig(filename='server.log',
					format='%(asctime)s | %(filename)s:%(lineno)d | %(funcName)s | %(levelname)s | %(message)s',
					level=logging.DEBUG)
logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))


def create_app():
	app = flask.Flask(__name__)  # static_folder="../dist/assets", template_folder="../dist"
	# app.secret_key = os.urandom(24)
	CORS(app, resources={r"/api/*": {'origins': '*'}, r"/auth/*": {'origins': '*'}})

	app.config.from_pyfile(os.path.join(os.getcwd(), 'config.cfg'))
	app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///" + os.path.join(os.getcwd(), 'database.db')

	db.init_app(app)

	from lucrum.api import api
	app.register_blueprint(api)

	from lucrum.banking2.plaid import plaid_setup
	app.register_blueprint(plaid_setup)

	return app


# noinspection PyUnreachableCode
def initialise_database():
	if False: server_data.load_accounts()
	if False: server_data.new_database()
	if False: server_data.populate_database()

	server_data.prebuilt.save_all()
	server_data.db.session.commit()
