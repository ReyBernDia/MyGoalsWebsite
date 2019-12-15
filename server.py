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


if __name__ == "__main__":

    app.debug = True
    app.jinja_env.auto_reload = app.debug
    connect_to_db(app)
    # point that we invoke the DebugToolbarExtension
    # Use the DebugToolbar
    DebugToolbarExtension(app)
    app.run(port=5001, host='0.0.0.0')
