from flask import Flask, render_template, redirect,url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Email
app = Flask(__name__)

# Set a secret key for session management (required for using flash messages)
app.config['SECRET_KEY'] = 'mysecretkey123' 
# Replace with a more secure random string in production

# MySQL database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:password@localhost/flask'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database
db = SQLAlchemy(app)

# Disable CSRF protection (optional for development, not recommended for production)
app.config['WTF_CSRF_ENABLED'] = False


# Create a simple user model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

class UserForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Submit')
#display the list of users
@app.route("/")
def index():
    users = User.query.all()
    return render_template("list_users.html", users=users)

#adding a new user
@app.route("/add_user", methods=['GET', 'POST'])
def add_user():
    form = UserForm()
    if form.validate_on_submit():
        user = User(name=form.name.data, email=form.email.data)
        db.session.add(user)
        db.session.commit()
        flash('User added successfully', 'success')
        return redirect(url_for('index'))
    return render_template('add_user.html', form=form)

@app.route("/update-user/<int:id>", methods=["GET", "POST"])
def update_user(id):
    user = User.query.get_or_404(id)
    form = UserForm(obj=user)

    if form.validate_on_submit():
        user.name = form.name.data
        user.email = form.email.data
        db.session.commit()
        flash('User updated successfully!')
        return redirect(url_for('index'))

    return render_template("update_user.html", form=form)
