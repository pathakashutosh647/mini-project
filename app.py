from datetime import datetime, timedelta
from flask import Flask, request, jsonify, render_template
from itsdangerous import URLSafeTimedSerializer
import time


app = Flask(_name_)


# Dummy user credentials for demonstration purposes
users = {
    'ashu': 'Xyz@123',
}

# Secret key for token generation
app.config['SECRET_KEY'] = 'abc-123-xyz'

# Token expiration time (in seconds)
TOKEN_EXPIRATION = 3600

# Generate token for a given username

def generate_token(username):
    serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    expires = datetime.utcnow() + timedelta(seconds=TOKEN_EXPIRATION)
    token_data = {'username': username, 'expires': expires.isoformat()}
    token = serializer.dumps(token_data)
    return token


# Verify the validity of a token
def verify_token(token):
    serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    try:
        data = serializer.loads(token, max_age=TOKEN_EXPIRATION)
        if 'username' in data and 'expires' in data:
            expiration_time = data['expires']
            if expiration_time >= datetime.utcnow():
                return True
        return False
    except:
        return False

# Authentication endpoint
@app.route('/login', methods=['POST'])
# Authentication endpoint
@app.route('/login', methods=['POST'])
def login():
    data = request.form
    username = data.get('username')
    password = data.get('password')

    if username in users and users[username] == password:
        # User authenticated successfully
        # Redirect to success page or return success message
        return "Login successful!"
    else:
        return jsonify({'error': 'Invalid credentials'}), 401



# Data endpoint - requires valid token
@app.route('/data', methods=['GET'])
def data():
    token = request.headers.get('Authorization')

    # Implement token verification logic
    if verify_token(token):
        return jsonify({'message': 'Successful'}), 200
    else:
        return jsonify({'error': 'Auth failed, token is invalid.'}), 401

# Home page
@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')

if _name_ == '_main_':
    app.debug = True
    app.run()
