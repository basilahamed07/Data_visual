from flask import jsonify, request
from werkzeug.security import generate_password_hash, check_password_hash
from models import db,Users,Project_name,Project_details,New_defects,Total_Defect_Status,Test_execution_status,Testers,TestCaseCreationStatus,DefectAcceptedRejected,BuildStatus
from flask_jwt_extended import create_access_token,jwt_required,get_jwt_identity,verify_jwt_in_request
import os



def register_router(app):
    # ------------------------for login and register the users --------------------------------
    #to register the users
    @app.route('/register', methods=['POST'])
    def register_user():

        #get the data from the json  file
        data = request.json
        #check if the data was correct or not
        if 'username' not in data or 'password' not in data:
            return jsonify({'error': 'Username and password required'}), 400
        
        #check if the username is present or not
        if Users.query.filter_by(username=data['username']).first():
            return jsonify({'error': 'User already exists'}), 400
        #create the password in encripted file
        hashed_password = generate_password_hash(data['password'])
        
        # adding the User table for username and password
        new_user = Users(username=data['username'], password=hashed_password)
        
        try:
            db.session.add(new_user)
            db.session.commit()
            return jsonify({'message': 'User registered successfully'}), 201
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500
        


    #login the users
    @app.route('/login', methods=['POST'])
    def login_user():
        data = request.json
        if 'username' not in data or 'password' not in data:
            return jsonify({'error': 'Username and password required'}), 400
        
        user = Users.query.filter_by(username=data['username']).first()
        print(user)
        print(user.id)
        if not user or not check_password_hash(user.password, data['password']):
            return jsonify({'error': 'Invalid credentials'}), 401
        
        access_token = create_access_token(identity=str(user.id))
        
        return jsonify({
            'message': 'Login successful',
            'access_token': access_token,
            'user': {
                'username': user.username,
                'userId': user.id,
            }
        }), 200
    
    # -------------------------------end of login and register the user ----------------------------


    # 
    # @verify_jwt_in_request()
    @app.route("/create-project", methods=["GET", "POST"])
    @jwt_required() 
    def create_project():
        user_id = get_jwt_identity()
        print("JWT user_id:", user_id)  # Debugging: check the JWT identity
        
        if request.method == "POST":
            data = request.json
            print("Received data:", data)  # Print the incoming request data
            
            if "project_name" not in data:
                return jsonify({"error": "Project name is required"}), 400
            
            project_name = data.get("project_name")
            project = Project_name(project_name=project_name, user_id=user_id)
            
            try:
                db.session.add(project)
                db.session.commit()
                return jsonify({"message": "Project created successfully", "user_id": user_id}), 201
            except Exception as e:
                db.session.rollback()
                return jsonify({"error": str(e)}), 500
        
        elif request.method == "GET":
            projects = Project_name.query.all()
            return jsonify({"projects": [project.to_dict() for project in projects]}), 200
                
        