from flask import Flask
from flask_pymongo import PyMongo
import json
from cfg import config

app = Flask(__name__)
app.config["MONGO_URI"] = config['mongo_uri']
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
	return "Log In Page"

@app.route("/signup")
def show_signup():
	return "Sign Up Page"
