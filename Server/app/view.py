from functools import wraps
from core import server
from flask import session, render_template, request, redirect, url_for, jsonify
from model import *
from datetime import timedelta
from flask_bcrypt import Bcrypt
from werkzeug import secure_filename
import os
import string

app = server.app
bcrypt = Bcrypt(app)

def login_required(f):
	@wraps(f)
	def deco(*args, **kwargs) :
		if 'userid' in session :
			return f(*args, **kwargs)
		print 'not in session'
		return redirect(url_for('login_page'))
	return deco

@app.before_request
def session_reset():
	session.modified = True
	session.permanent = True
	app.permanent_session_lifetime = timedelta(minutes=30)

@app.route('/',methods = ['GET'])
def main_page():	
	return render_template('index.html')

