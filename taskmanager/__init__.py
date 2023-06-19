# This will make sure to initialize our taskmanager application as a package,
# allowing us to use our own imports, as well as any standard imports.

import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Only import env.py if the file exists (this is for development vs production)
# noqa is used to stop any linting issues
if os.path.exists("env.py"):
    import env  # noqa


app = Flask(__name__)

app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DB_URL")

db = SQLAlchemy(app)

# This is imported last as it relies on the app and db variables above
# noqa is used to stop any linting issues
from taskmanager import routes  # noqa
