"""Movie Ratings."""

from jinja2 import StrictUndefined

from flask import (Flask, jsonify, render_template, redirect,
                   request, flash, session)
from flask_debugtoolbar import DebugToolbarExtension

from model import User, Rating, Movie, connect_to_db, db


app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# Normally, if you use an undefined variable in Jinja2, it fails
# silently. This is horrible. Fix this so that, instead, it raises an
# error.
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """Homepage."""
    # a = jsonify([1, 3])
    # return a
    return render_template("homepage.html")


@app.route("/users")
def user_list():
    """Show list of users."""

    users = User.query.all()
    return render_template("user_list.html", users=users)


@app.route('/register', methods=['GET'])
def register_form():
    """Registration form."""

    return render_template("register_form.html")


@app.route('/register-submit', methods=['POST'])
def register_process():
    """Submit registration."""

    email = request.form.get('email')
    password = request.form.get('password')

    # REPLACE THE FOLLOWING BLOCK WITH CLEANER, MORE PYTHONIC CODE

    user = User.query.filter_by(email=email)
    if user.all() == []:
        # if not user:
        user = User(email=email,
                    password=password)
        db.session.add(user)
        db.session.commit()
        flash("You're now registered, great success!")
    else:
        flash("You're already registered.")

    return redirect("/")


@app.route('/login', methods=['GET'])
def login_form():
    """Login form."""

    return render_template("login_form.html")


@app.route('/login-submit', methods=['POST'])
def login_process():
    """Process login."""

    email = request.form.get('email')
    password = request.form.get('password')

    user = User.query.filter_by(email=email).first()

    # REPLACE THE FOLLOWING BLOCK WITH CLEANER, MORE PYTHONIC CODE

    # At least this line is Pythonic now, need to flip conditional logic next
    if not user:    
        flash("There is no user with that email address in the system; please create an account.")
        return redirect("/register")
    else:
        if password == user.password:
            flash("You are logged in, great success!")
            return redirect("/")
        elif password != user.password:
             flash("Password does not match email address; please try again.")
             return redirect("/login")


if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True
    app.jinja_env.auto_reload = app.debug  # make sure templates, etc. are not cached in debug mode

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    connect_to_db(app)

    app.run(port=5000, host='0.0.0.0')
