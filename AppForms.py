from flask import Flask, render_template, request, session, escape
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

@app.route("/") # ruta por defecto para acceder al template
def index():
	return render_template("Index.html")

@app.route("/search") #Route para saber si existe un usuario o no
def search():
	if "username" in session:
		nickname = request.args.get("nickname")
		user = Users.query.filter_by(username = nickname).first()

		if user:
			return "The user found succesfully is: " + user.username + "<a href = 'http://localhost:8050'> Back to Index </a>" + "<a href = 'http://localhost:8050/logout'> or Logout</a>" 
		return "the user doesn't exist. <a href = 'http://localhost:8050'> Back to the main page</a>" 

	return "You must log in first <a href = 'http://localhost:8050/login'>Login here</a>"
	
@app.route("/Home") # Metodo para saber que se ha iniciado la sesion correctamente
def home():
	if "username" in session:
		return "Welcome Admin user %s" % escape(session["username"])

	return "You must log in first. <a href = 'http://localhost:8050/login'>Login here </a>"

# @app.route("/cookie/set")
# def set_cookie():
# 	resp = make_response(render_template("Index.html"))
# 	resp.set_cookie("username", "Jesus Linares")

# 	return resp

# @app.route("/cookie/read")
# def read_cookie():
# 	username = request.cookies.get("username", None)

# 	if  username == None:
# 		return "The cookie doesn't exist"
# 	return username	

@app.route("/signup", methods = ["GET", "POST"]) #Metodo para crear una nueva sesion
def signup():	
	if request.method == "POST":
		password_Encryp = generate_password_hash(request.form["password"], method = "sha256")
		new_user = Users(username  = request.form["username"], password = password_Encryp)
		db.session.add(new_user)
		db.session.commit()

		return "You've registred succesfully"

	return render_template("signup.html")

@app.route("/login", methods = ["GET", "POST"]) #Metodo para iniciar sesion
def login():	
	if request.method == "POST":
		user = Users.query.filter_by(username = request.form["username"]).first()

		if user and check_password_hash(user.password, request.form["password"]):
			session["username"] = user.username
			return "You're logeed in <a href = 'http://localhost:8050'>Continue</a>"

		return "Your data is invalid, check and <a href = 'http://localhost:8050/login'>try again</a>"

	return render_template("login.html")

@app.route("/logout") # Metodo para salir de la sesion
def logout():
	session.pop("username", None)

	if "username" == None:
		return "Not start sesion"
	return "You are logeed out <a href = 'http://localhost:8050'>Go to back index</a>"

app.secret_key = "1234" # Clave secreta para las cookies de mi sesion iniciada
if __name__ == "__main__":
	db.create_all()
	app.run(debug = True, host ='0.0.0.0', port = 8050)
