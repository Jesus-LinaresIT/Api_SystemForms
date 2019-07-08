from flask import Flask, render_template, request
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

@app.route("/signup", methods = ["GET", "POST"])
def signup():	
	if request.method == "POST":
		password_Encryp = generate_password_hash(request.form["password"], method = "sha256")
		new_user = Users(username  = request.form["username"], password = password_Encryp)
		db.session.add(new_user)
		db.session.commit()

		return "You've registred succesfully"

	return render_template("signup.html")

if __name__ == "__main__":
	db.create_all()
	app.run(debug = True, host ='0.0.0.0', port = 8050)

#Para mañana elaborar el metodo get y las funciones login y search