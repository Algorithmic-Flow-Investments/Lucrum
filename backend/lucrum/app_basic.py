import flask

from .database import db
import os


def basic_app():
	app = flask.Flask(__name__)
	app.config.from_pyfile(os.path.join(os.getcwd(), 'config.cfg'))
	db.init_app(app)
	return app
