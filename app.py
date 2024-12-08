from flask import Flask, request, jsonify
from pymongo import MongoClient
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)

# MongoDB connection URI
client = MongoClient(
    "mongodb+srv://phemanthkumar746:htnameh509h@data.psr09.mongodb.net/?retryWrites=true&w=majority&appName=Data"
)
db = client.myLoginDatabase  # Replace with your database name
users_collection = db["users"]  # Replace with your collection name

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()

    # Check if the username and password are provided
    if not data or 'username' not in data or 'password' not in data:
        return jsonify({
            "status": "failure",
            "message": "Username and password are required"
        }), 400

    username = data['username']
    password = data['password']
    email = data.get('email', None)  # email is optional

    # Hash the password
    hashed_password = generate_password_hash(password)

    # Create a new user document
    user = {
        'username': username,
        'email': email,
        'password': hashed_password
    }

    # Insert user into the MongoDB collection
    users_collection.insert_one(user)
    return jsonify({"status": "success", "message": "User registered successfully!"}), 201

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    # Check if the username and password are provided
    if not data or 'username' not in data or 'password' not in data:
        return jsonify({
            "status": "failure",
            "message": "Username and password are required"
        }), 400

    username = data['username']
    password = data['password']

    # Find the user in the database
    user = users_collection.find_one({'$or': [{'username': username}, {'email': username}]})

    if user:
        if check_password_hash(user['password'], password):
            return jsonify({"status": "success", "message": "Login successful"})
        else:
            return jsonify({"status": "failure","message": "Invalid password"}), 401
    else:
        return jsonify({"status": "failure","message": "Username not found"}), 401

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
