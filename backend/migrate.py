import os

from flask import Flask
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from lucrum import database
from lucrum.models import *

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///" + os.path.join(os.getcwd(), "database.db")

database.DB_FOREIGN_KEY_CONSTRAINTS = False

database.db.init_app(app)

migrate = Migrate(app, database.db, render_as_batch=True)

manager = Manager(app)
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
	manager.run()
