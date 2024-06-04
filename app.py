from models import Station, Network, User, db, connect_db
import requests, json
from flask import Flask, render_template

# get city from user input

# get https://api.citybik.es/v2/networks/?fields=location,id,company,name
# make a table with company, id, location.city, and name

# find instances with matching city and return ids
# for each id get https://api.citybik.es/v2/networks/<ID>?fields=stations

# make card with name and number of stations
# try to put all stations on a map?

NETWORKURL = "https://api.citybik.es/v2/networks/?fields=location,id,company,name"

# requests.get

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///citybikes'

connect_db(app)
with app.app_context():
    db.create_all()

@app.route("/")
def homepage():
    Network.query.delete()
    # clearing db to get all current networks in case API updates them
    
    res = requests.get("https://api.citybik.es/v2/networks/?fields=location,id,company,name")
    res = res.json()
    networks=res["networks"]

    for network in networks:
        newNetwork = Network(
            company = network["company"],
            id = network["id"],
            city = network["location"]["city"],
            name = network["name"]
        )
        db.session.add(newNetwork)

    db.session.commit()

    return render_template("index.html")
