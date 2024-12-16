from flask import jsonify, request
from models import db,Project_name,Testers
from flask_jwt_extended import jwt_required,get_jwt_identity
from datetime import date

#logic for get assign the month recoding to the date


#for get the project id for corrosponding project name
def get_project_name(project_name):
    project = Project_name.query.filter_by(project_name=project_name).first()
    return project



def billable_details_route(app):
     #in this function post only the name of the billable resources

    @app.route("/tester-billable", methods=["GET", "POST"])
    @jwt_required() 
    def tester_billable():
        user_id = get_jwt_identity()
        if request.method == "POST":
            data = request.json
            print("Received data:", data)  # Print the incoming request data
            
            if not data.get("tester_name"):
                return jsonify({"error": "tester_name not found"}), 404 
            
            tester_name = data.get("tester_name")


            
            new_billable_resources = Testers(tester_name=tester_name, user_id=user_id)

            try:        
                db.session.add(new_billable_resources)
                db.session.commit()
                return jsonify({"message": "tester details created successfully", "user_id": user_id}), 201
            except Exception as e:
                db.session.rollback()
                return jsonify({"error": str(e)}), 500
            
        elif request.method == "GET":
            projects = Testers.query.all()
            return jsonify({"testers": [tester.to_dict() for tester in projects]}), 200


    #for this put we want to use the update the project and billable or not
    # for here we all are update only project and billable when click the project details
    @app.route("/testers-billable/<int:id>", methods=["PUT"])
    @jwt_required()
    def update_tester(id):
        tester = Testers.query.get(id)
        if not tester:
            return jsonify({"error": "Tester not found"}), 404

        data = request.json
        print("Received data:", data)  # Print the incoming request data

        # If 'project_name' is provided, update project_name_id
        project_name = data.get("project_name")
        if project_name:
            # Assuming get_project_name() returns a Project_name object with an 'id' attribute
            project_name_id = get_project_name(project_name)  
            if project_name_id:
                # Assigning the project_name_id as a list (even if it's just a single ID)
                temp_number = tester.project_name_id
                tester.project_name_id = [temp_number,project_name_id.id]  # Ensure it's a list of integers
            else:
                return jsonify({"error": "Project name not found"}), 404

        # If 'billable' is provided, update the billable status
        billable = data.get("billable")
        if billable is not None:  # Check if billable is provided (could be a boolean)
            tester.billable = billable

        # Commit the changes to the database
        try:
            db.session.commit()
            return jsonify({"message": "Tester details updated successfully", "tester_id": tester.id}), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({"error": str(e)}), 500



# -------------------------------code by basil ---------------------------------


