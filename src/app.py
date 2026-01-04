"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
# from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# Create the jackson family object
jackson_family = FamilyStructure("Jackson")


@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code


@app.route('/')
def sitemap():
    return jsonify({"message": "API de la familia Jackson"})


# Generate sitemap with all your endpoints
@app.route('/members', methods=['GET'])
def get_all_members():
    members = jackson_family.get_all_members()
    return jsonify(members), 200


@app.route('/members/<int:member_id>', methods=['GET'])
def get_one_member(member_id):
    member = jackson_family.get_member(member_id)
    if member is None:
        return jsonify({"error": "Miembro no encontrado"}), 404
    # Quitamos last_name de la respuesta como piden las instrucciones
    response = {
        "id": member["id"],
        "first_name": member["first_name"],
        "age": member["age"],
        "lucky_numbers": member["lucky_numbers"]
    }
    return jsonify(response), 200


@app.route('/members', methods=['POST'])
def add_member():
    body = request.get_json()
    if not body:
        return jsonify({"error": "El cuerpo de la solicitud está vacío"}), 400
    if "first_name" not in body or "age" not in body or "lucky_numbers" not in body:
        return jsonify({"error": "Faltan campos obligatorios"}), 400
    if body["age"] <= 0:
        return jsonify({"error": "La edad debe ser mayor que 0"}), 400

    jackson_family.add_member(body)
    return jsonify({"message": "Miembro agregado"}), 200


@app.route('/members/<int:member_id>', methods=['DELETE'])
def delete_member(member_id):
    result = jackson_family.delete_member(member_id)
if not result:
        return jsonify({"error": "Miembro no encontrado"}), 404
    return jsonify({"done": True}), 200



# This only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
