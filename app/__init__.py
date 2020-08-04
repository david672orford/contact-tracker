#
# Copyright 2020 David Chappell
# This file is part of Content Tracker.
#
# Content Tracker is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Content Tracker is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Contact Tracker. If not, see <https://www.gnu.org/licenses/>.
#

from flask import Flask

app = Flask(__name__, instance_relative_config=True)
app.config.from_mapping(
	APP_DISPLAY_NAME = "Contact Tracker",
	SQLALCHEMY_DATABASE_URI = 'sqlite:///%s/contact_tracker.db' % app.instance_path,
	SQLALCHEMY_TRACK_MODIFICATIONS = False,
	FLASK_ADMIN_SWATCH = 'cerulean',
	)
app.config.from_pyfile('config.py')

from . import views
from . import cron
#from . import admin

