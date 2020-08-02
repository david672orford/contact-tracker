#! /usr/bin/env python3
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

# Under Apache mod-wsgi we have to add ourself to the Python path.
if __name__.startswith("_mod_wsgi_"):
	import os, sys
	sys.path.insert(0, os.path.dirname(__file__))

import logging
from app import app

logging.basicConfig(level=logging.DEBUG)

# For Docker or for standalone testing
if __name__ == "__main__":
	from werkzeug.serving import run_simple
	from werkzeug.middleware.proxy_fix import ProxyFix
	app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_for=1)
	run_simple('0.0.0.0', 5000, app, threaded=True)
