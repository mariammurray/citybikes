from models import Station, Network, User, db, connect_db
from forms import UserForm
import requests, json
from flask import Flask, render_template, session


NETWORKURL = "https://api.citybik.es/v2/networks/?fields=location,id,company,name"
CURR_USER_KEY = "curr_user"


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///citybikes'

connect_db(app)
with app.app_context():
    db.create_all()

res = requests.get("https://api.citybik.es/v2/networks/?fields=location,id,company,name")
res = res.json()
networks=res["networks"]

@app.before_request
def add_user_to_g():
    """If we're logged in, add curr user to Flask global."""

    if CURR_USER_KEY in session:
        g.user = User.query.get(session[CURR_USER_KEY])

    else:
        g.user = None

def do_login(user):
    """Log in user."""

    session[CURR_USER_KEY] = user.id

@app.route("/")
def homepage():

    return render_template("index.html", networks = networks)

@app.route("/<networkid>")
def displayCity(networkid):
    res = requests.get(f"https://api.citybik.es/v2/networks/{networkid}")
    res = res.json()
    network = res["network"]

    return render_template("city.html", networks = networks, nw = network)

@app.route('/signup', methods=["GET", "POST"])
def signup():

    form = UserForm()

    if form.validate_on_submit():
        try:
            user = User.register(
                username=form.username.data,
                password=form.password.data,
            )
            db.session.commit()

        except IntegrityError:
            flash("Username already taken", 'danger')
            return render_template('signup.html', form=form)

        do_login(user)

        return redirect("/")

    else:
        return render_template('signup.html', form=form)
    
@app.route('/login', methods=["GET", "POST"])
def login():

    form = UserForm()

    if form.validate_on_submit():
        user = User.authenticate(form.username.data,
                                 form.password.data)

        if user:
            do_login(user)
            return redirect("/")

        flash("Invalid credentials.", 'danger')

    return render_template('signup.html', form=form)
