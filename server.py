from flask import (
	Flask,
	abort, 
	render_template, 
	request, 
	redirect,
	session
)
import pymongo 
from flask_pymongo import PyMongo
from hashlib import sha256
import json
from cfg import config
from utils import get_rand_str
from datetime import datetime

app = Flask(__name__)
app.config["MONGO_URI"] = config['mongo_uri']
app.secret_key = b'jnfew890432'
mongo = PyMongo(app)

@app.route("/")
def show_index():
	if not 'userToken' in session:
		session['error'] = 'You must login to access this page'
		return redirect('/login')

	# Validate user token
	token_document = mongo.db.user_tokens.find_one({
		'sessionHash': session['userToken']
	})

	if token_document is None:
		session.pop('userToken', None)
		session['error'] = 'You must login again to access this page'
		return redirect('/login')

	userId = token_document['userId']

	user = mongo.db.users.find_one({
		'_id': userId
	})
	
	uploaded_files = mongo.db.files.find({
		'userId': userId,
		'isActive': True
	}).sort([("createdAt", pymongo.DESCENDING)])


	# TODO create an array with the formatted data to display on the home page below is an example
	# this is how we will show the data in the files.html page
	# will also need to fix the email at the top of the page	
	
	# formatted_file_data = []
	# for f in uploaded_files:
	#	f['formattedDate'] = datetime.strftime(f['createdAt'])
	#	formatted_file_data.append()

	# We will send the 'formated_file_data' to the render template function below in place of uploaded files

	return render_template(
		'files.html',
		uploaded_files=uploaded_files,
		user=user
	)

@app.route("/login")
def show_login():
	if 'userToken' in session:
		# TODO Validate user token from the database
		# TODO Redirect to / if session is valid
		pass

	signupSuccess = ''
	if 'signupSuccess' in session:
		signupSuccess = session['signupSuccess']
		# Just want to show once, after refresh we pop it
		session.pop('signupSuccess', None)

	error = ''
	if 'error' in session:
		error = session['error']
		#remove something from session
		session.pop('error', None)
	
	return render_template('login.html',
			signupSuccess=signupSuccess,
			error=error)

@app.route("/check_login", methods=["POST"])
def check_login():
	try:
		email = request.form['email']
	except KeyError:
		email = ''

	try:
		password = request.form['password']
	except:
		password = ''
	

	# Check if email is blank

	if not len(email) > 0:
		session['error'] = 'Email is required'
		return redirect('/login')

	# Check if password is blank
	if not len(password) > 0:
		session['error'] = 'Password is required'
		return redirect('/login')

	# Find email in database
	user_document = mongo.db.users.find_one({"email": email })
	if user_document is None:
		# user document with the given email is not found
		session['error'] = 'No account exists with this email address'
		return redirect('/login')


	# Verify that password hash matches with original
	password_hash = sha256(password.encode('utf-8')).hexdigest()
	if user_document['password'] != password_hash:
		session['error'] = 'Invalid password'
		return redirect('/login')

	# Generate token and save it in session\
	random_string = get_rand_str()
	randomSessionHash = sha256(random_string.encode('utf-8')).hexdigest()
	token_object = mongo.db.user_tokens.insert_one({
			'userId': user_document['_id'],
			'sessionHash': randomSessionHash,
			'createdAt': datetime.utcnow(),
		})

	session['userToken'] = randomSessionHash

	# If email and password are good we will redirect to index route
	return redirect('/')


@app.route("/signup")
def show_signup():
	error = ''
	if 'error' in session:
		error = session['error']
		#remove something from session
		session.pop('error', None)
	
	return render_template("signup.html", error=error)

@app.route("/handle_signup", methods=['POST'])
def handle_signup():
	try:
		email = request.form['email']
	except KeyError:
		email = ''
	try:
		password = request.form['password']
	except:
		password = ''

	# Check if email is blank
	if not len(email) > 0:
		session['error'] = 'Email is required'
		return redirect('/signup')


	# Check if email is valid
	# Look up regex to use here need to improve. Google python check if email is valid
	if not '@' in email or not '.' in email:
		session['error'] = 'Email is invalid'
		return redirect('/signup')


	# Check if password is blank
	if not len(password) > 0:
		session['error'] = 'Password is required'
		return redirect('/signup')

	# Check if email already exists
	matching_user_count = mongo.db.users.count_documents({"email": email })
	if matching_user_count > 0:
		session['error'] = 'Email already exists'
		# need to add a "forgot email or password" link
		return redirect('/signup')

	password = sha256(password.encode('utf-8')).hexdigest()

	#Check user record in database
	result = mongo.db.users.insert_one({
			'email': email,
			'password': password,
			'name': '',
			'lastLoginDate': None,
			'createdAt': datetime.utcnow(),
			'updatedAt': datetime.utcnow(),
		})

	#Redirect to Login page
	session['signupSuccess'] = 'Your user account is ready. You may now login!'
	return redirect('/login')

@app.route('/logout')
def logout_user():
	session.pop('userToken', None)
	session['signupSuccess'] = 'You are now logged out.'
	return redirect('/login')
