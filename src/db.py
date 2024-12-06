from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Area(db.Model):
    """
    Area Model
    """
    __tablename__ = "areas"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)
    locations = db.relationship("Location", back_populates="area")

    def __init__(self, **kwargs):
        """
        Initialize an Area object
        """
        self.name = kwargs.get("name")

    def serialize(self):
        """
        Serialize an Area object
        """
        return {
            "id": self.id,
            "name": self.name,
            "locations": [location.simple_serialize() for location in self.locations],
        }

    def simple_serialize(self):
        """
        Simple serialization of an Area object
        """
        return {
            "id": self.id,
            "name": self.name,
        }


class Location(db.Model):
    """
    Location Model
    """
    __tablename__ = "locations"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)
    area_id = db.Column(db.Integer, db.ForeignKey("areas.id"), nullable=False)
    area = db.relationship("Area", back_populates="locations")
    noise_level = db.Column(db.Integer, nullable=False) 
    traffic_level = db.Column(db.Integer, nullable=False) 
    open_hour = db.Column(db.String, nullable = False) #record containg start and end tiem
    require_reservation = db.Column(db.Boolean, nullable = False)

    def __init__(self, **kwargs):
        """
        Initialize a Location object
        """
        self.name = kwargs.get("name")
        self.area_id = kwargs.get("area_id")
        self.noise_level = kwargs.get("noise_level")
        self.traffic_level = kwargs.get("traffic_level")
        self.open_hour = kwargs.get("open_hour")
        self.require_reservation = kwargs.get("require_reservation")


    def simple_serialize(self):
        """
        Simple serialization of a Location object
        """
        return {
            "id": self.id,
            "name": self.name,
            "noise_level": self.noise_level,
            "traffic_level": self.traffic_level,
        }


class User(db.Model):
    """
    User Model
    """
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)
    preferences = db.Column(db.String, nullable=True)  #record containing noise&& traffic level 

    def __init__(self, **kwargs):
        """
        Initialize a User object
        """
        self.name = kwargs.get("name")
        self.preferences = kwargs.get("preferences")

    def serialize(self):
        """
        Serialize a User object
        """
        return {
            "id": self.id,
            "name": self.name,
            "preferences": self.preferences,
        }
