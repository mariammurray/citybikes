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

res = requests.get("https://api.citybik.es/v2/networks/?fields=location,id,company,name")
res = res.json()
networks=res["networks"]

@app.route("/")
def homepage():
    # res = requests.get("https://api.citybik.es/v2/networks/?fields=location,id,company,name")
    # res = res.json()
    # networks=res["networks"]

 # remove database component, just create network list directly from API
 # We pass the whole network list to HTML
 # We create options for the Serach text box and show suggestions
 # Once the user picks any one city, we gonna show network card downbelow
 # On clicking on a particular network card we gonna take him to a new tab with router /:networkname

    # for network in networks:
    #     newNetwork = Network(
    #         company = network["company"],
    #         id = network["id"],
    #         city = network["location"]["city"],
    #         name = network["name"]
    #     )
    #     db.session.add(newNetwork)

    # db.session.commit()

    # cities = []
    # for r in db.session.query(Network.city).all():
    #     city = r[0]
    #     cities.append(city)


    return render_template("index.html", networks = networks)

@app.route("/<networkid>")
def displayCity(networkid):
    res = requests.get(f"https://api.citybik.es/v2/networks/{networkid}")
    res = res.json()
    network = res["network"]

        # city: nw["location"]["city"],
        # country: nw["location"]["country"],
        # stations: [i["name"] for i in nw["stations"]]

    # matches = db.session.query(Network).filter(Network.city == cityname)

    return render_template("city.html", networks = networks, nw = network)
