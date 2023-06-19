from taskmanager import db


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # unique defines whether the string is unique or not
    # nullable enforces whether or not the field can have a null value 
    category_name = db.Column(db.String(25), unique=True, nullable=False)

    # db.relationship helps to create relationship between the Category table
    # and Task table as every task needs to be associated with a Category
    tasks = db.relationship(
        # table you wish to relate
        "Task", 
        # backref="this table in lowercase" back refeerence itself
        backref="category", 
        # all, delete means it will find all related items and delete them
        cascade="all, delete",
        # The last parameter here is lazy=True, which means that when we query 
        # the database for categories, it can simultaneously identify any task 
        # linked to the categories.
        lazy=True)


    def __repr__(self):
        # This is a standard python function meaning represent
        # Which means to represent the class objects as a string
        return self.category_name


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task_name = db.Column(db.String(50), unique=True, nullable=False)
    # Text allows us to use longer string strings than String
    task_description = db.Column(db.Text, nullable=False)
    is_urgent = db.Column(db.Boolean, default=False, nullable=False)
    # If you need to include Date and Time, you can use db.DateTime or db.Time
    due_date = db.Column(db.Date, nullable=False)
    category_id = db.Column(
        db.Integer, db.ForeignKey("category.id"), 
        # ondelete="CASCADE" 1 to many relationship with Category as each Task 
        # needs one Category If a Category is deleted then the tasks linked will 
        # also be deleted
        ondelete="CASCADE", 
        nullable=False
    )

    def __repr__(self):
        # This is a standard python function meaning represent
        # Which means to represent the class objects as a string

        # We can return a string using the .format() method
        # alternatively we can us the f string - 
        # f"#{self.id} - {self.task_name} | Urgent: {self.is_urgent}"
        return "#{0} - Task{1} | Urgent: {2}".format(
            self.id, self.task_name, self.is_urgent)

