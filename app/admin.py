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
	list_columns = ('id', 'date', 'user', 'canceled')

admin.add_view(UsersView(Users, db.session))
admin.add_view(ContactsView(Contacts, db.session))
admin.add_view(AlertsView(Alerts, db.session))

