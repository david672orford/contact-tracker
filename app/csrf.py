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

from flask import session, g
import secrets

from . import app

def csrf_token():
	if not 'token' in g:
		g.token = secrets.token_urlsafe()
		session['csrf_token'] = g.token
	return g.token
app.jinja_env.globals['csrf_token'] = csrf_token

def csrf_token_correct(request):
	correct_token = session.pop('csrf_token',None)
	form_token = request.form.get('csrf_token')
	return correct_token is not None and form_token is not None and form_token == correct_token

