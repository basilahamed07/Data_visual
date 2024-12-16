from flask import Flask, jsonify, request, abort
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
import datetime
import os
import secrets
from routing_two import register_router
# Initialize Flask app
app = Flask(__name__)

# Setup the secret key for JWT (you can use your own secret or an environment variable)
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', secrets.token_hex(32))  # Secure secret key
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = datetime.timedelta(hours=1)  # Access token expiration time (1 hour)

# Initialize JWTManager with the app
jwt = JWTManager(app)

register_router(app)
# Example route to create a JWT token (login route)


# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
