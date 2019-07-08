from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

import os

#dbDir = "sqlite:///" + os.path.abspath(os.getcwd()) + "/database.db"

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = dbDir
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

# class Posts(db.Model):
# 	id = db.Column(db.Integer, primary_key = True)
# 	titleD = db.Column(db.String(30))		

@app.route("/filePython/<string:project>/<string:user>")
def userA(project = "Project", user = "Linares"):
	title = "Welcome!!"
	return render_template("Index.html", title=title)


if __name__ == "__main__":
#	db.create_all()
	app.run(debug = True, host ='0.0.0.0', port = 8050)