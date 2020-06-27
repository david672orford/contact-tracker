from flask import request, render_template, make_response, redirect, session, url_for
from datetime import timedelta, date
import pyqrcode
from io import BytesIO

from . import app
from .models import db, Users
from .csrf import csrf_token_correct

@app.before_request
def make_session_permanent():
	session.permanent = True
	app.permanent_session_lifetime = timedelta(days=365)

# The user interface
@app.route("/")
def main():
	print(session)

	# If the visitor has a QR code number stored in a browser cookie,
	# load his user object from the database.
	user = None
	if 'my_code' in session:
		user = Users.query.filter_by(qr_code=session['my_code']).first()

	# If the visitor is a signed-up user and he has scanned a QR code
	# which we still have not recorded, do so now.
	other_user = None
	if user is not None and 'scanned_code' in session:
		other_user = Users.query.filter_by(qr_code=session['scanned_code']).first()
		if other_user is not None:
			today = date.today()
			db.session.add(Contacts(date=today, party1=user, party2=other_user))
			db.session.add(contact = Contacts(date=today, party1=other_user, party2=user))
			user.last = other_user.last = today
			db.session.commit()
		session.pop('scanned_code')

	# Render the main page from the template. If the user is signed up,
	# his QR code will be rendered.
	return render_template("main.html", user=user, other_user=other_user)

# The QR codes send the visitor to this URL. Save the code in our session
# cookie and send the user to the user interface where new users will be
# given the opportunity to receive a QR code.
@app.route("/s/<qr_code>")
def qr_code_scanned(qr_code):
	session['scanned_code'] = qr_code
	return redirect("/")

# User has asked to be assigned a QR code.
@app.route("/signup", methods=["POST"])
def signup():
	if csrf_token_correct(request):
		user = Users()
		db.session.add(user)
		db.session.commit()
		session['my_code'] = user.qr_code
	return redirect("/")

# Render the QR code as an SVG image
@app.route("/qr/<qr_code>")
def qr_code_renderer(qr_code):
	image = pyqrcode.create(url_for('qr_code_scanned', qr_code=qr_code))
	text = BytesIO()
	image.svg(text)
	response = make_response(text.getvalue())
	response.headers['Content-Type'] = 'image/svg+xml'
	return response

