import flask

from database import db


def basic_app():
	app = flask.Flask(__name__)
	app.config.from_pyfile('config.cfg')
	db.init_app(app)
	return app
