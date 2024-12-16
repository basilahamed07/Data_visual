from flask import jsonify, request
from werkzeug.security import generate_password_hash, check_password_hash
from models import db,Users,Project_name,Project_details,New_defects,Total_Defect_Status,Test_execution_status,Testers,TestCaseCreationStatus,DefectAcceptedRejected,BuildStatus
from flask_jwt_extended import create_access_token,jwt_required,get_jwt_identity,verify_jwt_in_request
import os



def register_router(app):
    @app.route('/login', methods=['POST'])
    def login():
        # For this example, we will use a static username and password check
        username = request.json.get('username', None)
        password = request.json.get('password', None)

        if username != "admin" or password != "password123":
            return jsonify({"msg": "Invalid username or password"}), 401

        # Create JWT token with the user's identity (username in this case)
        access_token = create_access_token(identity=username)
        return jsonify(access_token=access_token), 200

    # Example protected route that requires a valid JWT token
    @app.route('/protected', methods=['GET'])
    @jwt_required()  # This decorator ensures that a valid JWT is required to access this route
    def protected():
        # Get the current user's identity from the JWT token
        current_user = get_jwt_identity()
        print(current_user)

        # Return a response containing the logged-in user's information
        return jsonify(logged_in_as=current_user), 200

    # Decode and verify a JWT token manually (for educational purposes)
    # @app.route('/decode_token', methods=['GET'])
    # def decode_token():
    #     token = request.args.get('token')

    #     if not token:
    #         return jsonify({"msg": "Token is required"}), 400

    #     try:
    #         # Decode the JWT token
    #         decoded_token = jwt.decode_token(token)

    #         # Decode the payload manually (you can inspect the header and payload as needed)
    #         header = decoded_token.get('header')
    #         payload = decoded_token.get('payload')

    #         return jsonify({
    #             "header": header,
    #             "payload": payload
    #         })
    #     except Exception as e:
    #         return jsonify({"msg": "Invalid token", "error": str(e)}), 400
                
        