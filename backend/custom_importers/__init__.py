from esaver import main
from lucrum.app_basic import basic_app
from lucrum.database import db


# noinspection PyUnreachableCode
def run_importers():
	if True:
		return
	with basic_app().app_context():
		main()
		db.session.commit()
