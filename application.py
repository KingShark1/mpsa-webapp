from enum import unique
import json
import ast

from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey, Table, Column
from sqlalchemy.orm import relationship, declarative_base

from util import utils 
Base = declarative_base()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'

db = SQLAlchemy(app)

# class Association(db.Model):
# 	__tablename__ = "association"

# 	left_id = Column(ForeignKey("left.id"), primary_key=True)
# 	right_id = Column(ForeignKey("right.id"), primary_key=True)
# 	event = relationship("Events", back_populates="athletes")
# 	athlete = relationship("Athletes", back_populates="events")

class Athletes(db.Model):
	__tablename__ = "left"
	
	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	username = db.Column(db.String(80), nullable=False)
	date_of_birth = db.Column(db.String(12), nullable=False)
	age_group = db.Column(db.String(6), nullable=False)
	sex = db.Column(db.String(5), nullable=False)
	events = db.Column(db.String(300), nullable=False)

	def convert_str_to_list(self, str):
		print("inside convert str to list :", type(str))
		return ast.literal_eval(str)

	def __repr__(self):
		return f"""
Id : {self.id}
Username : {self.username}
Age Group : {self.date_of_birth[:4]}
Date of Birth : {self.date_of_birth}
Events : {self.events}"""

# class Events(db.Model):
# 	__tablename__ = "right"
	
# 	id = db.Column(db.Integer(), primary_key=True)
# 	name = db.Column(db.String(80), nullable=False) # Name should consist of event name + gender + age group
# 	athletes = relationship("Association", back_populates="event")

# 	def __repr__(self):
# 		return f"{self.name} {self.athletes}"


@app.route('/')
def index():
	return render_template('home.html')

@app.route('/register')
def register():
	return render_template('register.html')

@app.route('/result', methods=['POST', 'GET'])
def result():
	output = request.form.to_dict()
	name = output.pop('name')
	dob = output.pop('dob')
	sex = output.pop('sex')
	# output now has only events.
	events = list(output.keys())
	athlete = Athletes()

	athlete.username = name
	athlete.date_of_birth = dob	# in string format "yyyy-mm-dd"
	athlete.sex = sex
	athlete.age_group = utils.get_age_group_from_birthyear(int(dob[:4]))
	athlete.events = f'{events}'

	db.session.add(athlete)
	db.session.commit()
	print(athlete)
	return render_template("register.html", name=athlete.username)

@app.route('/all_athletes')
def show_athletes():
	output = Athletes.query.all()
	return render_template("all_athletes.html", athletes=output)

@app.route('/events')
def events():
	return render_template('events.html')
