from lucrum.app import create_app
from lucrum.processing.database_setup import setup
from custom_importers import run_importers

if __name__ == '__main__':
	setup()
	run_importers()
	app = create_app()
	app.run(debug=True, threaded=True, use_reloader=True, host='0.0.0.0')
