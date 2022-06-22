"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Planets, People, Favorites

#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/user', methods=['GET'])
def List_users():
    users = User.query.all()
    all_users = list(map(lambda user: user.serialize(), users))
    return jsonify(all_users)

@app.route('/user/favorites', methods=['GET'])
def List_favorites():
    favorites = Favorites.query.all()
    all_favorites = list(map(lambda favorite: favorite.serialize(), favorites))
    return jsonify(all_favorites)

# @app.route('/people' , methods=['POST']) 
# def create_people():
#     body = request.get_json()
#     people = People(name=body["name"],gender=body["gender"],height=body["height"],skin_color=body["skin_color"],hair_color=body["hair_color"])
#     db.session.add(people)
#     db.session.commit()

#     res = jsonify(people.serialize())
#     res.status_code = 201
#     return res

@app.route('/people', methods=['GET'])
def list_peoples():
    peoples = People.query.all()
    all_peoples = list(map(lambda people: people.serialize(), peoples))
    return jsonify(all_peoples)

@app.route('/planet', methods=['GET'])
def list_planets():
    planets = Planets.query.all()
    all_planets = list(map(lambda planet: planet.serialize(), planets))
    return jsonify(all_planets)

@app.route('/people/<int:people_id>' , methods=['GET']) 
def list_people(people_id):

    if request.method == 'GET':
        people = People.query.get(people_id)
        if people is None:
            raise APIException("Tarea no encontrada", 404)

        return jsonify(people.serialize())

@app.route('/planet/<int:planet_id>' , methods=['GET']) 
def list_planet(planet_id):

    if request.method == 'GET':
        planet = Planets.query.get(planet_id)
        if planet is None:
            raise APIException("Tarea no encontrada", 404)

        return jsonify(planet.serialize())
 
# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
