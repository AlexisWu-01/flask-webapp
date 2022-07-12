from markupsafe import escape
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from access_quantaq import append_sensor_data, update_sensor_list
from datetime import datetime

# from flask_mail import Message
# from flaskbb.extensions import mail, celery

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

db = SQLAlchemy(app)



class Post(db.Model):
	title = db.Column(db.Text(100), nullable=False, primary_key=True)
	content = db.Column(db.Text(2000), nullable=False)
	image = db.Column(db.String(20), default='default.jpg')
	data = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

	def __repr__(self):
    		return f"Post({self.title}, {self.content}, {self.image})"

@app.route('/')
def map_func():
	sensor_list = update_sensor_list("sensor_list.json")
	data = {}
	append_sensor_data(data)
	return render_template("map.html", sensor_list=sensor_list, data=data)

@app.route('/#close/reports/')
@app.route('/reports/')
def reports_func():
	return render_template("reports.html")

@app.route('/#close/explore')
@app.route('/explore')
def explore_func():
	return render_template("explore.html")

@app.route('/#close/forum')
@app.route('/forum')
def forum_func():
    return render_template("forum.html")


@app.route('/capitalize/<word>/')
def capitalize(word):
    return '<h1>{}</h1>'.format(escape(word.capitalize()))

if __name__ == "__main__":
	app.run(debug = True)


