from flask import request, render_template, make_response, redirect, session, abort, send_from_directory
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import NoResultFound
from datetime import timedelta, date
import logging
import pyqrcode, io

from . import app
from .models import db, Users, Alerts, Contacts
from .csrf import csrf_token_correct

logger = logging.getLogger(__name__)

# By default Flask sessions last until the browser window is closed. Here we
# make it last for one year. Otherwise the user would get a new QR code
# on every visit.
@app.before_request
def make_session_permanent():
	session.permanent = True
	app.permanent_session_lifetime = timedelta(days=365)

def load_user(required=True):
	try:
		return Users.query.filter_by(qr_code=session['my_code']).one()
	except NoResultFound:
		if required:
			abort(403)
		else:
			return None

# The user interface
@app.route("/")
def main():
	# If the visitor has a QR code number stored in a browser cookie,
	# load his user object from the database.
	user = None
	if 'my_code' in session:
		user = load_user(required=False)

	# If the visitor is a signed-up user and he has scanned a QR code
	# which we have not yet recorded, do so now.
	scan_result = 'NONE'
	if user is not None and 'scanned_code' in session:
		scanned_user = Users.query.filter_by(qr_code=session['scanned_code']).first()
		if scanned_user is not None:
			today = date.today()

			try:
				# Record the meeting for both parties
				db.session.add(Contacts(date=today, party1=user, party2=scanned_user))
				db.session.add(Contacts(date=today, party1=scanned_user, party2=user))

				# Update the last scan date for both users
				user.last = scanned_user.last = today

				db.session.commit()
				scan_result = 'RECORDED'

			except IntegrityError:
				logger.info("Duplicate scan")
				db.session.rollback()
				scan_result = 'DUP'

		session.pop('scanned_code')

	# Collect contact records where the 1st party has sent
	# an alert and we are the 2nd party.
	alerts_received = None
	if user is not None:
		alerts_received = Contacts.query.filter_by(party2_id=user.id).filter(Contacts.alert != None).all()

	# Render the main page from the template. If the user is signed up,
	# his QR code will be rendered.
	return render_template(
		"main.html",
		user=user,
		scan_result=scan_result,
		alerts_received=alerts_received,
		)

# The in-app scanner
@app.route("/scanner")
def scanner():
	return render_template("scanner.html")

# The QR codes send the visitor to this URL. Save the code in our session
# cookie and send the user to the user interface where new users will be
# given the opportunity to receive a QR code of their own.
@app.route("/s/<qr_code>")
def qr_code_scanned(qr_code):
	session['scanned_code'] = qr_code
	return redirect("/")

# The user has pressed the "Get my QR Code". We create a Users() object
# (which will include a randomly assigned number for the QR code) and save
# the QR code number in a long-lived cookie so we will recognize the user
# on future visits.
@app.route("/signup", methods=["POST"])
def signup():
	if csrf_token_correct(request):
		user = Users()
		db.session.add(user)
		db.session.commit()
		session['my_code'] = user.qr_code
	return redirect("/")

# The user has pressed the "Send an Alert" button.
@app.route("/alerts/send", methods=["POST"])
def alerts_send():
	if csrf_token_correct(request):
		user = load_user()
		today = date.today()
		cutoff = (today - timedelta(days=14))
		try:
			alert = Alerts(date=today, user=user)
			db.session.add(alert)
			for contact in Contacts.query.filter_by(party1_id=user.id).filter(Contacts.date >= cutoff):
				contact.alert = alert
			db.session.commit()
		except IntegrityError:
			logger.info("Duplicate alert")	
			db.session.rollback()
	else:
		logger.info("Incorrect CSRF token")
	return redirect("/#tab2")

# The users has pressed the "Cancel this Alert" or "Restore this Alert" button.
@app.route("/alerts/set-canceled", methods=["POST"])
def alerts_set_cancel():
	if csrf_token_correct(request):
		alert_id, alert_canceled = request.form.get('alert').split("-")
		alert_canceled = bool(int(alert_canceled))
		alert = Alerts.query.filter_by(user=load_user(), id=alert_id).one()
		alert.canceled = alert_canceled
		db.session.commit()
	else:
		logger.info("Incorrect CSRF token")
	return redirect("/#tab2")

# Render the QR code as an SVG image
@app.route("/static/qr/<qr_code>")
def qr_code_renderer(qr_code):
	image = pyqrcode.create("%s/s/%s" % (app.config['CANONICAL_URL'], qr_code))
	text = io.BytesIO()
	image.svg(text)
	response = make_response(text.getvalue())
	response.headers['Content-Type'] = 'image/svg+xml'
	return response

@app.route("/service-worker.js")
def service_worker():
	return send_from_directory(app.root_path, "service-worker.js", mimetype="text/javascript")

