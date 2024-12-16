from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv
import os
from models import db

from main_routing import all_router
import secrets
import datetime

#to load the env file
load_dotenv()


#to initilize the flask app
app = Flask(__name__)


#configuraction for dtatabase connecttion

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#get the security key for csrf prdaction
app.secret_key = os.getenv("SECRET_KEY")  # Required for forms (CSRF protection)

#for get the jwd tokens
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', secrets.token_hex(32))  # Secure secret key
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = datetime.timedelta(hours=1)  # Access token expiration time (1 hour)

# Initialize JWTManager with the app
jwt = JWTManager(app)

db.init_app(app)
migrate = Migrate(app, db)

CORS(app)


#for regiser the router in app

all_router(app)

#for api routing by using the register routing

with app.app_context():
    db.create_all()

if __name__=="__main__":
    app.run(debug=True,host="0.0.0.0",port=5000)
