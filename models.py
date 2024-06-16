
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy

bcrypt = Bcrypt()
db = SQLAlchemy()


def connect_db(app):
    """Connect to database."""
    db.app = app
    db.init_app(app)

#following from my schema might be unecessary:
# Table cityStations {
#   id integer [primary key]
#   city text
# }

# Ref: cityStations.id < stations.id



class Station(db.Model):
    __tablename__= "stations"

    id = db.Column(db.Integer, primary_key= True)
    address = db.Column(db.Text)
    network_id = db.Column(db.Text, db.ForeignKey('networks.id', ondelete="cascade"))

class Network(db.Model):
    __tablename__= "networks"

    id = db.Column(db.Text, primary_key= True)
    name = db.Column(db.Text)
    city = db.Column(db.Text)
    company = db.Column(db.Text)

class User(db.Model):
    __tablename__= "users"

    id = db.Column(db.Integer, primary_key= True)
    username = db.Column(db.Text, unique=True)
    password = db.Column(db.Text,nullable=False)

    # favStations = db.relationship(
    #     "Stations",
    #     secondary="favourites",
    #     primaryjoin=(favourites.user_id == id),
    #     secondaryjoin=(favourites.station_id == id)
    # )
    @classmethod
    def register(cls, username, password):

        encrypted_pwd = bcrypt.generate_password_hash(password).decode('UTF-8')
        
        user = User(
            username = username,
            password = encrypted_pwd
        )
        db.session.add(user)
        return user
    
    @classmethod
    def authenticate(cls, username, password):
        user = cls.query.filter_by(username=username).first()

        if user:
            is_auth = bcrypt.check_password_hash(user.password, password)
            if is_auth:
                return user

        return False

class Favourites(db.Model):
    __tablename__= "favourites"

    user_id = db.Column(db.Integer,db.ForeignKey('users.id', ondelete="cascade"),primary_key=True)
    station_id = db.Column(db.Integer,db.ForeignKey('stations.id', ondelete="cascade"),primary_key=True)

