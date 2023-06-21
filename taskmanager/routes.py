from flask import render_template, request, redirect, url_for
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
    return render_template("tasks.html")


@app.route("/categories")
def categories():
    # categories = db.session.query(Category).order_by(Category.category_name)

    # The all() returns a cursor object so we can wrap in a list() to convert
    # it to a Python list so it can be used in our template as a list
    categories = list(Category.query.order_by(Category.category_name).all())
    return render_template("categories.html", categories=categories)


@app.route("/add_category", methods=["GET", "POST"])
def add_category():
    # Handling the GET and POST methods with if statement
    if request.method == "POST":
        category = Category(
            category_name=request.form.get("category_name")
        )
        db.session.add(category)
        db.session.commit()
        return redirect(url_for("categories"))
    # By default this handles the GET method
    return render_template("add_category.html")

# using custom paths we can cast it as a str: or as an int: noqa


@app.route("/edit_category/<int:category_id>", methods=["GET", "POST"])
# we also pass the custom path/variable into the function below
def edit_category(category_id):

    # we can use the get_or_404 method in order to bring back the specific
    # id or produce a 404 message if not found
    category = Category.query.get_or_404(category_id)
    if request.method == "POST":
        # if method is POST then set the called category(.category_name) above
        # to the request.form.get()
        category.category_name = request.form.get("category_name")
        db.session.commit()
        # remember to return your redirects
        return redirect(url_for("categories"))

    # default GET method
    return render_template("edit_category.html", category=category)


@app.route("/delete_category/<int:category_id>")
def delete_category(category_id):
    category = Category.query.get_or_404(category_id)
    db.session.delete(category)
    db.session.commit()
    return redirect(url_for("categories"))
