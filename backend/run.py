from lucrum.app import create_app
from lucrum.processing.database_setup import setup

if __name__ == '__main__':
	setup()
	app = create_app()
	app.run(debug=True, threaded=True, use_reloader=True, host='0.0.0.0')
