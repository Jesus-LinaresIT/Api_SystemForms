from flask import Flask, render_template, request, make_response
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

import os

dbDir = "sqlite:///" + os.path.abspath(os.getcwd()) + "/database.db"

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = dbDir
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

class Users(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	username = db.Column(db.String(50), unique = True, nullable = False)
	password = db.Column(db.String(50), nullable = False)

@app.route("/")
def index():
	return render_template("index.html")

@app.route("/cookie/set")
def set_cookie():
	resp = make_response(render_template("Index.html"))
	resp.set_cookie("username", "Jesus Linares")

	return resp

@app.route("/cookie/read")
def read_cookie():
	username = request.cookies.get("username", None)

	if  username == None:
		return "The cookie doesn't exist"
	return username	

@app.route("/search")
def search():
	nickname = request.args.get("nickname")
	user = Users.query.filter_by(username = nickname).first()

	if user:
		return "The user found succesfully is: " + user.username 
	return "the user doesn't exist" 

@app.route("/signup", methods = ["GET", "POST"])
def signup():	
	if request.method == "POST":
		password_Encryp = generate_password_hash(request.form["password"], method = "sha256")
		new_user = Users(username  = request.form["username"], password = password_Encryp)
		db.session.add(new_user)
		db.session.commit()

		return "You've registred succesfully"

	return render_template("signup.html")

@app.route("/login", methods = ["GET", "POST"])
def login():	
	if request.method == "POST":
		user = Users.query.filter_by(username = request.form["username"]).first()

		if user and check_password_hash(user.password, request.form["password"]):
			return "You're logeed in"

		return "Your data is invalid, check and try again"

	return render_template("login.html")

if __name__ == "__main__":
	db.create_all()
	app.run(debug = True, host ='0.0.0.0', port = 8050)

#Para mañana elaborar el metodo get y las funciones login y search