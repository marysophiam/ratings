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


#go to registration form
@app.route('/register', methods=["GET"])
def register_form():
    """     """

    return render_template("register_form.html")


#submit registration
@app.route('/register', methods=["POST"])
def register_process():
    """      """

    email = request.form.get('email')
    password = request.form.get('password')

    user_query = User.query.filter_by(email=email)
    if user_query.all() == []:
    #if not user_query....
        user_query = User(email=email,
                          password=password)
        db.session.add(user_query)
        db.session.commit()
        flash("Thank you for registering!")
    else:
        flash("You are already registered!")

    return redirect("/")
    #####CODE checks if the user is in the database... if not add new user
    # once new user added ... redirect user to the homepage




#go to login form
@app.route('/login', methods=["GET"])
def login_form():
    """     """

    return render_template("login_form.html")


#submit registration
@app.route('/login', methods=["POST"])
def login_process():
    """      """

    email = request.form.get('email')
    password = request.form.get('password')

    user_query = User.query.filter_by(email=email).first()


    if not user_query:
        #if not user....
        flash("YOU ARE NOT IN THE SYSTEM - please register")
        return redirect("/")
    else:
        if password == user_query.password:
            # login success
            flash("Thank you for Logging In!")
            return redirect("/")
            #then log user in ---
            #(add their user id picked up from Database to the FLASK session)

        elif password != user_query.password:
             flash("Incorrect password Try again")
             return redirect("/login")



    #if email matches password:
        #then log user in ---
        #(add their user id picked up from Databaseto the FLASK session)






if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True
    app.jinja_env.auto_reload = app.debug  # make sure templates, etc. are not cached in debug mode

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    #Lines below needs to stay for app to work! all else commented out to remove debugger.
    connect_to_db(app)

    app.run(port=5000, host='0.0.0.0')
