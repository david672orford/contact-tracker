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

