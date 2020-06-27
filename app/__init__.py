from flask import Flask

app = Flask(__name__, instance_relative_config=True)
app.config.from_mapping(
	APP_DISPLAY_NAME = "Contact Tracker",
	SQLALCHEMY_DATABASE_URI = 'sqlite:///%s/contact_tracker.db' % app.instance_path,
	SQLALCHEMY_TRACK_MODIFICATIONS = False,
	FLASK_ADMIN_SWATCH = 'cerulean',
	)
app.config.from_pyfile('config.py')

from . import admin
from . import views

