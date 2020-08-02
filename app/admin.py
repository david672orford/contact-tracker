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

from flask_admin import Admin
from flask_admin.contrib.sqla.view import ModelView as InsecureModelView
from flask_admin.form import SecureForm
from . import app
from .models import db, Users, Contacts, Alerts

admin = Admin(app, name=app.config['APP_DISPLAY_NAME'])

# Create base model view
class ModelView(InsecureModelView):
    form_base_class = SecureForm
    action_disallowed_list = ['delete']     # no mass delete
    page_size = 15

class UsersView(ModelView):
	list_columns = ('id', 'qr_code', 'last')

class ContactsView(ModelView):
	list_columns = ('id', 'date', 'party1', 'party2', 'alert')

class AlertsView(ModelView):
	list_columns = ('id', 'date', 'user', 'contacts', 'canceled')

admin.add_view(UsersView(Users, db.session))
admin.add_view(ContactsView(Contacts, db.session))
admin.add_view(AlertsView(Alerts, db.session))

