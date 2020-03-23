from flask import Flask
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from lucrum.database import db
from lucrum.models import *

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

db.init_app(app)

migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
	manager.run()
