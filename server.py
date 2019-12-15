from jinja2 import StrictUndefined
from sqlalchemy import asc, update
from flask import Flask, render_template, redirect, request, flash, session, g
from flask_debugtoolbar import DebugToolbarExtension

from model import connect_to_db, db, Users, Goals

app = Flask(__name__)
# Required to use Flask sessions and the debug toolbar
app.secret_key = "QWEASDZXC"

#set to strict to avoid silent fails for undefined variables. 
app.jinja_env.undefined = StrictUndefined

@app.route("/")
def display_homepage():
    """Render homepage."""

    return render_template("homepage.html")

@app.route('/register', methods=['GET'])
def register_new_user():
    """Display user registration form."""

    return render_template("registration.html")

@app.route('/register', methods=['POST'])
def process_registration():
    """Register new user if email not already in db."""

    first_name = request.form.get('f_name')
    last_name = request.form.get('l_name')
    email = request.form.get('email')
    password = request.form.get('password')
    
    # if user email already exists, ignore
    if Users.query.filter(Users.email == email).first():
        pass
    else: 
        user = Users(f_name=first_name, 
                     l_name=last_name, 
                     email=email, 
                     password=password)
        db.session.add(user)
        db.session.commit()
    # if user email does not exist, add to db
    return redirect('/')

@app.route('/login', methods=['GET'])
def display_login_page():
    """Display login page."""

    return render_template("login.html")

@app.route('/login', methods=['POST'])
def login_user():
    """Process login for user."""

    #query email and password in database. 
    email = request.form.get('email')
    password = request.form.get('password')

    user = Users.query.filter((Users.email == email),
                              (Users.password == password)).first()

    if user:
    #if matches, log in user (add user_id to flask session)
        session['user_id'] = user.user_id
        # flash- logged in
        flash("Successfully logged in!")
        #redirect to homepage
        return redirect('/user-page')
    else: 
        flash("That is not a valid email & password.")
        return redirect('/login')   

@app.route('/logout')
def logout_user():
    """Remove user from session and logout."""

    del session['user_id']
    flash("Successfully logged out!")

    return redirect('/')

@app.route('/user-page')
def display_user_page():
    """Show specific information about user."""

    user = Users.query.filter(Users.user_id == session['user_id']).first()
    
    return render_template('user_page.html', 
                            user=user)

@app.route('/add_new', methods=['POST'])
def add_new_goal():
    """Process adding a new goal for a user."""

    goal = request.form.get('goal')
    user_id = session['user_id']

    new_goal = Goals(user_id=user_id,
                     u_goal=goal)
    db.session.add(new_goal)
    db.session.commit()

    flash("New Goal Added!")
    return redirect('/user-page')

@app.route('/edit_goal', methods=['POST'])
def edit_goal():
    """Edit existing user goal."""

    goal = request.form.get('goal')
    goal_id = request.form.get('goal_id')

    edit_goal = Goals.query.filter(Goals.goal_id == goal_id).one()

    edit_goal.u_goal = goal
    db.session.add(edit_goal)
    db.session.commit()

    flash("You edited your goal!")
    return redirect('/user-page')

if __name__ == "__main__":

    app.debug = True
    app.jinja_env.auto_reload = app.debug
    connect_to_db(app)
    # point that we invoke the DebugToolbarExtension
    # Use the DebugToolbar
    DebugToolbarExtension(app)
    app.run(port=5001, host='0.0.0.0')
