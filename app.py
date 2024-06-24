from models import User, db, connect_db, Favourite
from forms import UserForm
import requests
from flask import Flask, render_template, session, g, redirect, flash
from sqlalchemy.exc import IntegrityError


NETWORKURL = "https://api.citybik.es/v2/networks/?fields=location,id,company,name"
CURR_USER_KEY = "curr_user"


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///citybikes'
app.config['SECRET_KEY'] = "secret"

connect_db(app)
with app.app_context():
    db.create_all()

res = requests.get("https://api.citybik.es/v2/networks/?fields=location,id,company,name")
res = res.json()
networks=res["networks"]

@app.before_request
def add_user_to_g():

    if CURR_USER_KEY in session:
        g.user = User.query.get(session[CURR_USER_KEY])

    else:
        g.user = None


@app.route("/")
def homepage():

    return render_template("index.html", networks = networks)

@app.route("/<networkid>")
def displayCity(networkid):
    data = []
    network = []
    res = requests.get(f"https://api.citybik.es/v2/networks/{networkid}")
    data = res.json()
    network = data["network"]

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

        session[CURR_USER_KEY] = user.id

        return redirect("/")

    else:
        return render_template('signup.html', form=form)

    
@app.route('/logout')
def logout():
    """Handle logout of user."""

    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")
    
    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]

    return redirect("/login")
    
@app.route('/login', methods=["GET", "POST"])
def login():

    form = UserForm()

    if form.validate_on_submit():
        user = User.authenticate(form.username.data,
                                 form.password.data)

        if user:
            session[CURR_USER_KEY] = user.id
            return redirect("/")

        flash("Invalid credentials.", 'danger')

    return render_template('signup.html', form=form, networks = networks)

@app.route("/<networkid>/<stationid>")
def addStation(networkid, stationid):
    user = User.query.get(session[CURR_USER_KEY])
    if user:
        fav = Favourite(
            user_id = user.id,
            station_id = stationid,
            network_id = networkid
        )
        db.session.add(fav)
        db.session.commit()
    else:
        flash("Log in", "danger")
        return redirect("/")
    

    return redirect("/favourites")

@app.route("/favourites")
def showFavourites():
    favs = db.session.query(Favourite).filter(Favourite.user_id == session[CURR_USER_KEY]).all()
    favArr = []
    for i in favs:
        res = requests.get(f"https://api.citybik.es/v2/networks/{i.network_id}")
        data = res.json()
        station = [station for station in data["network"]["stations"] if station["id"] == i.station_id]
        favArr+=station

    return render_template("favourites.html", networks = networks, favourites = favArr)