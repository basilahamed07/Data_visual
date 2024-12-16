from flask import jsonify, request
from werkzeug.security import generate_password_hash, check_password_hash
from models import db,Users,Project_name,Project_details,New_defects,Total_Defect_Status,Test_execution_status,Testers,TestCaseCreationStatus,DefectAcceptedRejected,BuildStatus
from flask_jwt_extended import create_access_token,jwt_required,get_jwt_identity
import os
from datetime import date

#logic for get assign the month recoding to the date


#for get the project id for corrosponding project name
def get_project_name(project_name):
    project = Project_name.query.filter_by(project_name=project_name).first()
    return project



# convert the date into month
def get_month(date_str):
    if len(date_str) > 10:
        date_obj = date.fromisoformat(date_str[0:10])
        return date_obj.strftime('%B')
    else:
        date_obj = date.now()
        return date_obj.strftime('%B')



def project_details_route(app):
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

            if Project_name.query.filter_by(project_name=project_name).first():
                return jsonify({"error": "Project name already exists"}), 400
            
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
                



# -----------------------------------------code ----------------------------------------------------
    @app.route("/update-project/<int:id>", methods=["PUT"])
    @jwt_required()
    def update_project(id):
        user_id = get_jwt_identity()
        print(f"JWT user_id: {user_id}")  # Debugging: check the JWT identity

        # Fetch the project by ID
        project = Project_name.query.get(id)

        
        if not project:
            return jsonify({"error": "Project not found"}), 404
        
        # Ensure the current user is the owner of the project
        if project.user_id != int(user_id):
            return jsonify({"error": "You are not authorized to update this project"}), 403
        
        # Get the data from the request
        data = request.json
        print("Received data:", data)  # Debugging: print the incoming request data

        # Update the project details if provided in the request
        if "project_name" in data:
            project.project_name = data["project_name"]
        
        try:
            db.session.commit()
            return jsonify({"message": "Project updated successfully"}), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({"error": str(e)}), 500
                
        # Route to create new project details
    @app.route("/create-project-details", methods=["POST"])
    @jwt_required()
    def create_project_details():
        user_id = get_jwt_identity()
        
        data = request.json
        print("Received data:", data)  # Debugging: print the incoming request data
        
        # Required fields
        required_fields = ["project_name_id", "RAG", "tester_count", "billable", "nonbillable", 
                           "billing_type", "RAG_details"]
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"{field} is required"}), 400
        
        # Create a new Project_details object
        project_detail = Project_details(
            project_name_id=data["project_name_id"],
            RAG=data["RAG"],
            tester_count=data["tester_count"],
            billable=data["billable"],
            nonbillable=data["nonbillable"],
            billing_type=data["billing_type"],
            automation=data.get("automation", False),
            ai_used=data.get("ai_used", False),
            RAG_details=data["RAG_details"],
            user_id=user_id
        )
        
        try:
            db.session.add(project_detail)
            db.session.commit()
            return jsonify({"message": "Project details created successfully"}), 201
        except Exception as e:
            db.session.rollback()
            return jsonify({"error": str(e)}), 500

    # Route to get all project details for a user
    @app.route("/project-details", methods=["GET"])
    @jwt_required()
    def get_project_details():
        user_id = get_jwt_identity()
        
        project_details = Project_details.query.filter_by(user_id=user_id).all()
        
        return jsonify({"project_details": [project.to_dict() for project in project_details]}), 200

    # Route to update project details
    @app.route("/update-project-details/<int:id>", methods=["PUT"])
    @jwt_required()
    def update_project_details(id):
        user_id = int(get_jwt_identity())
        
        data = request.json
        project_detail = Project_details.query.get(id)

        print(project_detail.user_id)
        
        if not project_detail:
            return jsonify({"error": "Project details not found"}), 404
        print(f"user_id: {project_detail.user_id}")
        
        if project_detail.user_id != int(user_id):
            return jsonify({"error": "You are not authorized to update this project detail"}), 403
        
        # Update project detail fields
        if "project_name_id" in data:
            project_detail.project_name_id = data["project_name_id"]
        if "RAG" in data:
            project_detail.RAG = data["RAG"]
        if "tester_count" in data:
            project_detail.tester_count = data["tester_count"]
        if "billable" in data:
            project_detail.billable = data["billable"]
        if "nonbillable" in data:
            project_detail.nonbillable = data["nonbillable"]
        if "billing_type" in data:
            project_detail.billing_type = data["billing_type"]
        if "automation" in data:
            project_detail.automation = data["automation"]
        if "ai_used" in data:
            project_detail.ai_used = data["ai_used"]
        if "RAG_details" in data:
            project_detail.RAG_details = data["RAG_details"]
        
        try:
            db.session.commit()
            return jsonify({"message": "Project details updated successfully"}), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({"error": str(e)}), 500

    # Route to delete project details
    @app.route("/delete-project-details/<int:id>", methods=["DELETE"])
    @jwt_required()
    def delete_project_details(id):
        user_id = get_jwt_identity()
        
        project_detail = Project_details.query.get(id)

        
        if not project_detail:
            return jsonify({"error": "Project details not found"}), 404
        
        if project_detail.user_id != int(user_id):
            return jsonify({"error": "You are not authorized to delete this project detail"}), 403
        
        try:
            db.session.delete(project_detail)
            db.session.commit()
            return jsonify({"message": "Project details deleted successfully"}), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({"error": str(e)}), 500
        
    
    
    # ------------------------code by basil------------------------