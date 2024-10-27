from flask import Flask, request, jsonify

app = Flask(__name__)

# Predefined users
users = {
    "bindu": "bindu123",
    "joe": "joe44",
    "gem": "gem56"
}

# Login route accepting POST requests only
@app.route('/login', methods=['POST'])
def login():
    # Ensure the request body is JSON
    if not request.is_json:
        return jsonify({"message": "Request body must be JSON"}), 400
    
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    # Check if both username and password are provided
    if not username or not password:
        return jsonify({'message': "Username and password are required"}), 400
    
    # Validate credentials
    if username in users and users[username] == password:
        return jsonify({'message': "Login successful"}), 200
    else:
        return jsonify({"message": "Invalid username or password"}), 401

# Route to get all users (for demonstration/testing purposes)
@app.route('/users', methods=['GET'])
def get_users():
    return jsonify(users), 200

if __name__ == '__main__':
    app.run(debug=True)
