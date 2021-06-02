from flask import (
	Flask,
	abort, 
	render_template, 
	request, 
	redirect,
	session
)
from flask_pymongo import PyMongo
from hashlib import sha256
import json
from cfg import config
from datetime import datetime

app = Flask(__name__)
app.config["MONGO_URI"] = config['mongo_uri']
app.secret_key = b'jnfew890432'
mongo = PyMongo(app)

@app.route("/")
def show_home():
	user_documents = mongo.db.users.find({})
	print(user_documents)

	for doc in user_documents:
		print(doc)

	return "Home Page"

@app.route("/login")
def show_login():
	signupSuccess = ''
	if 'signupSuccess' in session:
		signupSuccess = session['signupSuccess']
		# Just want to show once, after refresh we pop it
		session.pop('signupSuccess', None)
	
	return render_template('login.html', signupSuccess=signupSuccess)

@app.route("/check_login", methods=["POST"])
def check_login():
	email = request.form['email']
	password = request.form['password']

	user_documents = mongo.db.users.find({"email": email })

	print('Email is : ' + email)
	print('Password is : ' + password)
	return 'I should now check email ' + email + ' and password'


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

	print(email)
	print(password)

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
