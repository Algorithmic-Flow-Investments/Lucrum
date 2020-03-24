from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import event, MetaData
from sqlalchemy.engine import Engine


@event.listens_for(Engine, 'connect')
def set_sqlite_pragma(dbapi_connection, connection_record):
	cursor = dbapi_connection.cursor()
	cursor.execute('PRAGMA foreign_keys=ON')
	cursor.execute('PRAGMA journal_mode=WAL')
	cursor.close()


naming_convention = {
	"ix": 'ix_%(column_0_label)s',
	"uq": "uq_%(table_name)s_%(column_0_name)s",
	"ck": "ck_%(table_name)s_%(column_0_name)s",
	"fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
	"pk": "pk_%(table_name)s"
}

db = SQLAlchemy(metadata=MetaData(naming_convention=naming_convention))
