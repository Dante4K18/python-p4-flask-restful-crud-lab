#!/usr/bin/env python3

from flask import Flask, jsonify, request, make_response
from flask_migrate import Migrate
from flask_restful import Api, Resource

from models import db, Plant

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///plants.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)

api = Api(app)


class Plants(Resource):

    def get(self, id):
        plant = Plant.query.get(id)
        if not plant:
            return {'error': 'Plant not found'}, 404

        return plant.to_dict(), 200
    
    def post(self):
        data = request.get_json()

        new_plant = Plant(
            name=data['name'],
            image=data['image'],
            price=data['price'],
        )

        db.session.add(new_plant)
        db.session.commit()

        return make_response(new_plant.to_dict(), 201)

def patch(self, id):
        plant = Plant.query.get(id)
        if not plant:
            return {'error': 'Plant not found'}, 404

        data = request.get_json()
        if 'is_in_stock' in data:
            plant.is_in_stock = data['is_in_stock']

        db.session.commit()
        return jsonify(plant.to_dict())


api.add_resource(Plants, '/plants')


class PlantByID(Resource):

    def get(self, id):
        plant = Plant.query.filter_by(id=id).first().to_dict()
        return make_response(jsonify(plant), 200)


api.add_resource(PlantByID, '/plants/<int:id>')

@app.route('/plants/<int:id>', methods=['GET'])
def get_plant(id):
    plant = Plant.query.get(id)
    if not plant:
        return jsonify({"error": "Plant not found"}), 404
    return jsonify({
        "id": plant.id,
        "name": plant.name,
        "price": plant.price,
        "created_at": plant.created_at,
    }), 200


@app.route('/plants/<int:id>', methods=['PATCH'])
def update_plant(id):
    plant = Plant.query.get_or_404(id)  # Fetch the plant by ID
    data = request.get_json()          # Parse the JSON payload

    # Update fields (in this case, 'is_in_stock')
    if 'is_in_stock' in data:
        plant.is_in_stock = data['is_in_stock']

    db.session.commit()  # Save changes to the database

    # Return the updated plant as JSON
    return jsonify({
        "id": plant.id,
        "name": plant.name,
        "image": plant.image,
        "price": plant.price,
        "is_in_stock": plant.is_in_stock
    }), 200

@app.route('/plants/<int:id>', methods=['DELETE'])
def delete_plant(id):
    plant = Plant.query.get_or_404(id)  # Fetch the plant by ID

    db.session.delete(plant)  # Delete the plant
    db.session.commit()       # Commit changes to the database

    # Return an empty response with 204 status
    return '', 204


if __name__ == '__main__':
    app.run(port=5555, debug=True)
