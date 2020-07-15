# Schema of Contract Tracker's Database

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

# This object represents an anonymous user and his QR code.
class Users(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	qr_code = db.Column(db.String(), unique=True, default=generate_qr_code)
	last = db.Column(db.Date)
	contacts = db.relationship('Contacts', foreign_keys="[Contacts.party1_id]")
	alerts = db.relationship('Alerts')
	def __str__(self):
		return '<Users id=%s qr_code="%s">' % (self.id, self.qr_code)

# A pair of these objects represents a meeting between two users as recorded
# by one of them scanning the other's QR code, one object for each party.
class Contacts(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	date = db.Column(db.Date)
	party1_id = db.Column(db.Integer, db.ForeignKey('users.id'))
	party1 = db.relationship('Users', foreign_keys=[party1_id], back_populates='contacts')
	party2_id = db.Column(db.Integer, db.ForeignKey('users.id'))
	party2 = db.relationship('Users', foreign_keys=[party2_id])
	alert_id = db.Column(db.Integer, db.ForeignKey('alerts.id'))
	alert = db.relationship('Alerts', back_populates='contacts', cascade='all')
	# Only allow one contact record per day for any two users.
	__table_args__ = (db.UniqueConstraint('date','party1_id','party2_id'),)
	def __str__(self):
		return '<Contacts id=%s date=%s party1=%s party2=%s alert=%s>' % (self.id, self.date, self.party1, self.party2, self.alert)

# This object represents an alert. It is attached to recent Contacts()
# objects to which the alerter is party1.
class Alerts(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	date = db.Column(db.Date)
	user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
	user = db.relationship('Users', back_populates='alerts')
	canceled = db.Column(db.Boolean, default=False)
	contacts = db.relationship('Contacts', back_populates='alert')
	# Only allow one alert per user, per day.
	__table_args__ = (db.UniqueConstraint('date','user_id'),)
	def __str__(self):
		return '<Alerts id=%s date=%s user=%s canceled=%s>' % (self.id, self.date, self.user, self.canceled)

db.create_all()
