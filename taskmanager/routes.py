from flask import render_template, request, redirect, url_for, session, flash
from taskmanager import app, db
# import the model classes that are responsible for generating the tables
from taskmanager.models import Category, Task, User
from werkzeug.security import generate_password_hash, check_password_hash

# remember to create the database directly in postgresql -
# command line psql
# CREATE DATABASE taskmanager;
# connect to the database \c taskmanager;
# then once connected we can quit the CLI \q

# once created open the python CLI and write the following
# from task manager import db


@app.route("/")
def home():
    # we can order by here or in the rendered page with jinja
    tasks = list(Task.query.order_by(Task.due_date).all())
    return render_template("tasks.html", tasks=tasks)

# CATEGORY ROUTES


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

# TASK ROUTES


@app.route("/add_task", methods=["GET", "POST"])
def add_task():
    if "user" not in session:
        flash("You need to be logged in to add a task")
        return redirect(url_for("home"))
    # categories called to use in a dropdown list
    categories = list(Category.query.order_by(Category.category_name).all())
    if request.method == "POST":
        task = Task(
            task_name=request.form.get("task_name"),
            task_description=request.form.get("task_description"),
            is_urgent=bool(True if request.form.get("is_urgent") else False),
            due_date=request.form.get("due_date"),
            # Category ID, which will be generated as a dropdown list to choose
            # from, using the 'categories' list above.
            category_id=request.form.get("category_id"),
            user_id=session["user_id"]
        )
        db.session.add(task)
        db.session.commit()
        # remember that we do not send directly to the route but to the function
        # name
        return redirect(url_for("home"))
    # in order to display our categories in the template we need to pass it in
    # as an argument
    return render_template("add_task.html", categories=categories)


@app.route("/edit_task/<int:task_id>", methods=["GET", "POST"])
def edit_task(task_id):
    task = Task.query.get_or_404(task_id)
    categories = list(Category.query.order_by(Category.category_name).all())

    if "user" not in session or session["user"] != task["created_by"]:
        flash("You can only edit your own tasks!")
        return redirect(url_for("get_tasks"))

    if request.method == "POST":
        task.task_name = request.form.get("task_name")
        task.task_description = request.form.get("task_description")
        task.is_urgent = bool(True if request.form.get("is_urgent") else False)
        task.due_date = request.form.get("due_date")
        task.category_id = request.form.get("category_id")
        task.user_id = session["user_id"]
        db.session.commit()

        return redirect(url_for("home"))

    return render_template("edit_task.html", task=task, categories=categories)


@app.route("/delete_task/<int:task_id>")
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)

    if "user" not in session or session["user"] != task["user_id"]:
        flash("You can only delete your own tasks!")
        return redirect(url_for("home"))

    db.session.delete(task)
    db.session.commit()
    return redirect(url_for("home"))

# User Authentication


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        # check if username already exists in db
        existing_user = User.query.filter(
            User.username == request.form.get("username").lower()).all()

        if existing_user:
            flash("Username already exists")
            return redirect(url_for("register"))

        user = User(
            username=request.form.get("username").lower(),
            password=generate_password_hash(request.form.get("password"))
        )

        db.session.add(user)
        db.session.commit()

        session["user"] = request.form.get("username").lower()
        flash("Registration Successful!")
        return redirect(url_for("profile", username=session["user"]))

    return render_template("register.html")


@app.route("/profile/<username>", methods=["GET", "POST"])
def profile(username):

    if "user" in session:
        return render_template("profile.html", username=session["user"])

    flash("You are not currently logged in")
    return redirect(url_for("login"))


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # check if username exists in db
        existing_user = User.query.filter(
            User.username == request.form.get("username").lower()).all()

        if existing_user:
            # ensure hashed password matches user input
            if check_password_hash(
                    existing_user[0].password, request.form.get("password")):
                session["logged_in"] = True
                session["user"] = request.form.get("username").lower()
                session["user_id"] = existing_user[0].id
                flash("Welcome, {}".format(
                    request.form.get("username")))
                return redirect(url_for(
                    "profile", username=session["user"]))
            else:
                # invalid password match
                flash("Incorrect Username and/or Password")
                return redirect(url_for("login"))

        else:
            # username doesn't exist
            flash("Incorrect Username and/or Password")
            return redirect(url_for("login"))

    return render_template("login.html")


@app.route("/logout")
def logout():
    flash("You have been logged out")
    # remove user from session cookie
    session.pop("logged_in")
    session.pop("user")
    session("user_id")
    return redirect(url_for("login"))
