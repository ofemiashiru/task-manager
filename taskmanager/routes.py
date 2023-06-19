from flask import render_template
from taskmanager import app, db
# import the model classes that are responsible for generating the tables
from taskmanager.models import Category, Task

# remember to create the database directly in postgresql -
# command line psql
# CREATE DATABASE taskmanager;
# connect to the database \c taskmanager;
# then once connected we can quit the CLI \q

# once created open the python CLI and write the following 
# from task manager import db

@app.route("/")
def home():
    return render_template("base.html")