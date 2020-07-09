from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.engine import Engine
from sqlalchemy import event
import secrets
import string

from app import app

db = SQLAlchemy(app)

@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
	cursor = dbapi_connection.cursor()
	cursor.execute("PRAGMA foreign_keys=ON")
	cursor.close()

# Create a random 12-digit identifier for a user
def generate_qr_code():
	return ''.join(secrets.choice(string.digits) for i in range(12))

class Users(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	qr_code = db.Column(db.String(), unique=True, default=generate_qr_code)
	last = db.Column(db.Date)
	contacts = db.relationship('Contacts', foreign_keys="[Contacts.party1_id]")
	alerts = db.relationship('Alerts')
	def __str__(self):
		return '<Users id=%s code="%s">' % (self.id, self.code)

class Contacts(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	date = db.Column(db.Date)
	party1_id = db.Column(db.Integer, db.ForeignKey('users.id'))
	party1 = db.relationship('Users', foreign_keys=[party1_id], back_populates='contacts')
	party2_id = db.Column(db.Integer, db.ForeignKey('users.id'))
	party2 = db.relationship('Users', foreign_keys=[party2_id])
	alert = db.Column(db.Integer, db.ForeignKey('alerts.id'))

class Alerts(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	date = db.Column(db.Date)
	user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
	user = db.relationship('Users', back_populates='alerts')
	canceled = db.Column(db.Boolean, default=False)

db.create_all()
