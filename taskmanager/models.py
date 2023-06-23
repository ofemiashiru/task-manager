from taskmanager import db

class User(db.Model):
    # schema for user
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(250), nullable=False)

    def __repr__(self):
        return self.username

class Category(db.Model):
    # schema for the Category model
    id = db.Column(db.Integer, primary_key=True)
    # unique defines whether the string is unique or not
    # nullable enforces whether or not the field can have a null value
    category_name = db.Column(db.String(25), unique=True, nullable=False)
    # db.relationship helps to create relationship between the Category table
    # and Task table as every task needs to be associated with a Category
    # table you wish to relate
    # backref="this table in lowercase" back refeerence itself
    # all, delete means it will find all related items and delete them
    # The last parameter here is lazy=True, which means that when we query
    # the database for categories, it can simultaneously identify any task
    # linked to the categories.

    tasks = db.relationship("Task", backref="category", cascade="all, delete", lazy=True)

    def __repr__(self):
        # __repr__ to represent itself in the form of a string
        # This is a standard python function meaning represent
        # Which means to represent the class objects as a string
        return self.category_name


class Task(db.Model):
    # schema for the Task model
    id = db.Column(db.Integer, primary_key=True)
    task_name = db.Column(db.String(50), unique=True, nullable=False)
    task_description = db.Column(db.Text, nullable=False)
    is_urgent = db.Column(db.Boolean, default=False, nullable=False)
    due_date = db.Column(db.Date, nullable=False)

    # Text allows us to use longer string strings than String
    # If you need to include Date and Time, you can use db.DateTime or db.Time
    # ondelete="CASCADE" 1 to many relationship with Category as each Task
    # needs one Category If a Category is deleted then the tasks linked will
    # also be deleted
    category_id = db.Column(
        db.Integer, 
        db.ForeignKey("category.id", ondelete="CASCADE"), nullable=False
    )

    # This is a standard python function meaning represent
    # Which means to represent the class objects as a string

    # We can return a string using the .format() method
    # alternatively we can us the f string -
    # f"#{self.id} - {self.task_name} | Urgent: {self.is_urgent}"
    def __repr__(self):
        # __repr__ to represent itself in the form of a string
        return "#{0} - Task: {1} | Urgent: {2}".format(
            self.id, self.task_name, self.is_urgent
        )