from db import db
from flask import Flask

from db import db, Area, Location, User
from flask import Flask, request, jsonify

app = Flask(__name__)
db_filename = "cms.db"

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///%s" % db_filename
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True

db.init_app(app)
with app.app_context():
    db.create_all()

# Routes for Area
@app.route("/areas/", methods=["GET"])
def get_areas():
    areas = Area.query.all()
    return jsonify([area.serialize() for area in areas]), 200

@app.route("/areas/", methods=["POST"])
def create_area():
    data = request.get_json()
    name = data.get("name")
    if not name:
        return jsonify({"error": "Missing name"}), 400

    new_area = Area(name=name)
    db.session.add(new_area)
    db.session.commit()
    return jsonify(new_area.serialize()), 201

@app.route("/areas/<int:area_id>/", methods=["DELETE"])
def delete_area(area_id):
    area = Area.query.get(area_id)
    if not area:
        return jsonify({"error": "Area not found"}), 404

    db.session.delete(area)
    db.session.commit()
    return jsonify({"message": "Area deleted"}), 200

# Routes for Location
@app.route("/locations/", methods=["GET"])
def get_locations():
    locations = Location.query.all()
    return jsonify([location.simple_serialize() for location in locations]), 200

@app.route("/locations/", methods=["POST"])
def create_location():
    data = request.get_json()
    name = data.get("name")
    area_id = data.get("area_id")
    noise_level = data.get("noise_level")
    traffic_level = data.get("traffic_level")
    open_hour = data.get("open_hour")
    require_reservation = data.get("require_reservation")

    if not all([name, area_id, noise_level, traffic_level, open_hour, require_reservation is not
    None]):
        return jsonify({"error": "Missing required fields"}), 400

    new_location = Location(
    name=name,
    area_id=area_id,
    noise_level=noise_level,
    traffic_level=traffic_level,
    open_hour=open_hour,
    require_reservation=require_reservation,
        )
    db.session.add(new_location)
    db.session.commit()
    return jsonify(new_location.simple_serialize()), 201

@app.route("/locations/<int:location_id>/", methods=["DELETE"])
def delete_location(location_id):
    location = Location.query.get(location_id)
    if not location:

        return jsonify({"error": "Location not found"}), 404

    db.session.delete(location)
    db.session.commit()
    return jsonify({"message": "Location deleted"}), 200

# Routes for User
@app.route("/users/", methods=["GET"])
def get_users():
    users = User.query.all()
    return jsonify([user.serialize() for user in users]), 200

@app.route("/users/", methods=["POST"])
def create_user():
    data = request.get_json()
    name = data.get("name")
    preferences = data.get("preferences")

    if not name:
        return jsonify({"error": "Missing name"}), 400

    new_user = User(name=name, preferences=preferences)
    db.session.add(new_user)
    db.session.commit()
    return jsonify(new_user.serialize()), 201

@app.route("/users/<int:user_id>/", methods=["DELETE"])
def delete_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": "User deleted"}), 200



areas_data = [
    {"name": "North Campus"},
    {"name": "South Campus"},
    {"name": "West Campus"},
    {"name": "Central Campus"},
]

locations_data = [
    {
        "name": "RPCC",
        "area_name": "North Campus",
        "noise_level": 1,
        "traffic_level": 3,
        "open_hour": "08:00-22:00",
        "require_reservation": False,
    },
    {
        "name": "Olin Library",
        "area_name": "Central Campus",
        "noise_level": 3,
        "traffic_level": 7,
        "open_hour": "07:00-20:00",
        "require_reservation": False,
    },
]

# Populate the database
def seed_data():
    with app.app_context():
        db.drop_all()  
        db.create_all() 

        # Add areas
        areas = {}
        for area_data in areas_data:
            area = Area(name=area_data["name"])
            db.session.add(area)
            areas[area_data["name"]] = area  
        db.session.commit() 

        # Add locations
        for loc_data in locations_data:
            location = Location(
                name=loc_data["name"],
                area_id=areas[loc_data["area_name"]].id,  
                noise_level=loc_data["noise_level"],
                traffic_level=loc_data["traffic_level"],
                open_hour=loc_data["open_hour"],
                require_reservation=loc_data["require_reservation"],
            )
            db.session.add(location)

        db.session.commit()  
        print("Database loaded successfully!")

@app.route("/seed/", methods=["POST"])
def seed():
    seed_data()  
    return jsonify({"message": "Database loaded successfully"}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)

