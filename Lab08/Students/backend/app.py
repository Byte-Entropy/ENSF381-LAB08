from copy import deepcopy
from pathlib import Path

import joblib
import pandas as pd
from flask import Flask, jsonify, request
from flask_cors import CORS

SEEDED_USERS = {
    "1": {"id": "1", "first_name": "Ava", "user_group": 11},
    "2": {"id": "2", "first_name": "Ben", "user_group": 22},
    "3": {"id": "3", "first_name": "Chloe", "user_group": 33},
    "4": {"id": "4", "first_name": "Diego", "user_group": 44},
    "5": {"id": "5", "first_name": "Ella", "user_group": 55},
}

MODEL_PATH = Path(__file__).resolve().parent / "src" / "random_forest_model.pkl"
PREDICTION_COLUMNS = [
    "city",
    "province",
    "latitude",
    "longitude",
    "lease_term",
    "type",
    "beds",
    "baths",
    "sq_feet",
    "furnishing",
    "smoking",
    "cats",
    "dogs",
]

app = Flask(__name__)
CORS(app)
users = deepcopy(SEEDED_USERS)



# GET /users
@app.route("/users", methods=["GET"])
def get_users():
    return jsonify(list(users.values())), 200

# POST /users
@app.route("/users", methods=["POST"])
def create_user():
    data = request.get_json()
    if not data or "id" not in data or "first_name" not in data or "user_group" not in data:
        return jsonify({"message": "Missing id, first_name, or user_group."}), 400
    user_id = str(data["id"])
    if user_id in users:
        return jsonify({"message": f"User {user_id} already exists."}), 409
    user = {
        "id": user_id,
        "first_name": data["first_name"],
        "user_group": data["user_group"]
    }
    users[user_id] = user
    response = user.copy()
    response["message"] = f"Created user {user_id}."
    return jsonify(response), 201

# PUT /users/<user_id>
@app.route("/users/<user_id>", methods=["PUT"])
def update_user(user_id):
    data = request.get_json()
    if not data or "first_name" not in data or "user_group" not in data:
        return jsonify({"message": "Missing first_name or user_group."}), 400
    if user_id not in users:
        return jsonify({"message": f"User {user_id} was not found."}), 404
    users[user_id]["first_name"] = data["first_name"]
    users[user_id]["user_group"] = data["user_group"]
    response = users[user_id].copy()
    response["message"] = f"Updated user {user_id}."
    return jsonify(response), 200

# DELETE /users/<user_id>
@app.route("/users/<user_id>", methods=["DELETE"])
def delete_user(user_id):
    if user_id not in users:
        return jsonify({"message": f"User {user_id} was not found."}), 404
    del users[user_id]
    return jsonify({"message": f"Deleted user {user_id}."}), 200


if __name__ == "__main__":
    app.run(debug=True, port=5050)
