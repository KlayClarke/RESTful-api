import os
import random
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, jsonify, render_template, request

app = Flask(__name__)
app.secret_key = os.environ.get('FLASK_SECRET_KEY')

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


db.create_all()
all_cafes = db.session.query(Cafe).all()
success_json = {'response': {'success': 'Successfully added the new cafe.'}}
error_json = {'error': {'Not Found': 'Sorry, we don\'t have a cafe at that location.'}}


@app.route("/")
def home():
    return render_template("index.html")


@app.route('/add', methods=['POST'])
def add_cafe():
    new_cafe = Cafe(name=request.form.get('name'), map_url=request.form.get('map_url'),
                    img_url=request.form.get('img_url'),
                    location=request.form.get('location'), seats=request.form.get('seats'),
                    has_toilet=bool(request.form.get('has_toilet')),
                    has_wifi=bool(request.form.get('has_wifi')),
                    has_sockets=bool(request.form.get('has_sockets')),
                    can_take_calls=bool(request.form.get('can_take_calls')),
                    coffee_price=request.form.get('coffee_price'))
    db.session.add(new_cafe)
    db.session.commit()
    return jsonify(success_json)


@app.route('/search', methods=['GET'])
def search_for_cafes():
    location = request.args.get('location')
    cafes_near_location = db.session.query(Cafe).filter_by(location=location.title()).all()
    cafes = [cafe.to_dict() for cafe in cafes_near_location]
    if len(cafes_near_location) == 0:
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


@app.route('/update-price/<cafe_id>', methods=['PATCH'])
def update_price(cafe_id):
    selected_cafe = db.session.query(Cafe).filter_by(id=cafe_id).first()
    if selected_cafe is None:
        return jsonify(error_json), 404
    else:
        selected_cafe.coffee_price = request.args.get('new_price')
        db.session.commit()
        return jsonify(success_json), 200


if __name__ == '__main__':
    app.run(debug=True)
