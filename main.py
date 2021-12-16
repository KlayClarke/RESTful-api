import random
from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy

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

    def to_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}


all_cafes = db.session.query(Cafe).all()


@app.route("/")
def home():
    return render_template("index.html")


@app.route('/search/<location>', methods=['GET'])
def search_for_cafes(location):
    cafes_near_location = db.session.query(Cafe).filter_by(location=location.title()).all()
    cafes = [cafe.to_dict() for cafe in cafes_near_location]
    if len(cafes_near_location) == 0:
        error_json = {'error': {'Not Found': 'Sorry, we don\'t have a cafe at that location.'}}
        return jsonify(error_json)
    else:
        return jsonify(cafes=cafes)


@app.route('/all', methods=['GET'])
def get_all_cafes():
    cafes = [cafe.to_dict() for cafe in all_cafes]
    return jsonify(cafes=cafes)


@app.route('/random', methods=['GET'])
def get_random_cafe():
    random_cafe = random.choice(all_cafes)
    return jsonify(cafe=random_cafe.to_dict())


# HTTP GET - Read Record

# HTTP POST - Create Record

# HTTP PUT/PATCH - Update Record

# HTTP DELETE - Delete Record


if __name__ == '__main__':
    app.run(debug=True)
