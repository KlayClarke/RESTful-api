import random
from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy, _ident_func

app = Flask(__name__)

# Connect to Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


# Cafe TABLE Configuration
class Cafe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    map_url = db.Column(db.String(500), nullable=False)
    img_url = db.Column(db.String(500), nullable=False)
    location = db.Column(db.String(250), nullable=False)
    seats = db.Column(db.String(250), nullable=False)
    has_toilet = db.Column(db.Boolean, nullable=False)
    has_wifi = db.Column(db.Boolean, nullable=False)
    has_sockets = db.Column(db.Boolean, nullable=False)
    can_take_calls = db.Column(db.Boolean, nullable=False)
    coffee_price = db.Column(db.String(250), nullable=True)


all_cafes = db.session.query(Cafe).all()
num_of_cafes = len(all_cafes)


@app.route("/")
def home():
    return render_template("index.html")


@app.route('/random', methods=['GET'])
def get_random_cafe():
    random_num = random.randint(1, num_of_cafes)
    random_cafe = db.session.query(Cafe).get(random_num)
    rc = random_cafe
    return jsonify(can_take_calls=rc.can_take_calls, coffee_price=rc.coffee_price, has_sockets=rc.has_sockets,
                   has_toilet=rc.has_toilet, has_wifi=rc.has_wifi, id=rc.id, img_url=rc.img_url, location=rc.location,
                   map_url=rc.map_url, name=rc.name, seats=rc.seats)


# HTTP GET - Read Record

# HTTP POST - Create Record

# HTTP PUT/PATCH - Update Record

# HTTP DELETE - Delete Record


if __name__ == '__main__':
    app.run(debug=True)
