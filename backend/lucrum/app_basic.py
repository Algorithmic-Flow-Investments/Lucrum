import flask

from .database import db
import os


def basic_app():
	app = flask.Flask(__name__)
	app.config.from_pyfile(os.path.join(os.getcwd(), 'config.cfg'))
	app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///" + os.path.join(os.getcwd(), 'database.db')
	db.init_app(app)
	return app
