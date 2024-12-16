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
    if len(date_str) >= 9:
        date_obj = date.fromisoformat(date_str[0:10])
        return date_obj.strftime('%B')
    else:
        date_obj = date.now()
        return date_obj.strftime('%B')



def test_details_route(app):
    

# for New_defects model form apis  for form 1 table one 
    @app.route('/new_defects', methods=['GET', 'POST'])
    @jwt_required()
    def manage_defects():
        if request.method == 'GET':
            # Handle GET request: Fetch all defects
            defects = New_defects.query.all()
            return jsonify([defect.to_dict() for defect in defects])

        elif request.method == 'POST':
            # Handle POST request: Create a new defect
            data = request.json

            # Required fields for POST request
            required_fields = ['date', 'months', 'regression_defect', 'functional_defect', 'defect_reopened', 'uat_defect','project_name_id']

            # Check if all required fields are present in the request body
            for field in required_fields:
                if field not in data:
                    return jsonify({"error": f"Missing required field: {field}"}), 400


            #for date convenstion
            date_in_month = get_month(data['date'])
            project_id = get_project_name(data['project_name_id']).id

            # Create new defect from the provided data
            new_defect = New_defects(
                date=data['date'],
                months=date_in_month,
                regression_defect=data['regression_defect'],
                functional_defect=data['functional_defect'],
                defect_reopened=data['defect_reopened'],
                uat_defect=data['uat_defect'],
                project_name_id=project_id,
                user_id=int(get_jwt_identity())
            )

            # Add the new defect to the database
            db.session.add(new_defect)
            db.session.commit()

            return jsonify(new_defect.to_dict()), 201  # Return created defect with a 201 status

    # API endpoint to handle PUT and DELETE for '/new_defects/<int:id>'
    @app.route('/new_defects/<int:id>', methods=['PUT', 'DELETE'])
    @jwt_required()
    def update_or_delete_new_defect(id):
        # Get the defect by ID
        defect = New_defects.query.get_or_404(id)

        if request.method == 'PUT':
            # If the method is PUT, update the defect
            data = request.json

            # Required fields for PUT request
            required_fields = ['date', 'months', 'regression_defect', 'functional_defect', 'defect_reopened', 'uat_defect',     'project_name_id']

            # Check if all required fields are present in the request body
            for field in required_fields:
                if field not in data:
                    return jsonify({"error": f"Missing required field: {field}"}), 400
                
            date_in_month = get_month(data['date'])
            project_id = get_project_name(data['project_name_id']).id

            # Update the defect fields
            defect.date = data['date']
            defect.months = date_in_month
            defect.regression_defect = data['regression_defect']
            defect.functional_defect = data['functional_defect']
            defect.defect_reopened = data['defect_reopened']
            defect.uat_defect = data['uat_defect']
            defect.project_name_id = project_id
            defect.user_id = int(get_jwt_identity())

            # Commit changes to the database
            db.session.commit()
            return jsonify(defect.to_dict())

        elif request.method == 'DELETE':
            # If the method is DELETE, remove the defect
            db.session.delete(defect)
            db.session.commit()
            return '', 204  # Return an empty response after successful deletion


# for form 2 in testcase details table
    @app.route('/test_execution_status', methods=['GET', 'POST'])
    @jwt_required()
    def manage_test_execution_status():
        if request.method == 'GET':
            # Handle GET request: Fetch all test execution statuses
            test_statuses = Test_execution_status.query.all()
            return jsonify([status.to_dict() for status in test_statuses])

        elif request.method == 'POST':
            # Handle POST request: Create a new test execution status
            data = request.json

            # Required fields for POST request
            required_fields = ['months', 'date', 'total_execution', 'tc_execution', 'pass_count', 'fail_count', 'no_run',   'blocked', 'project_name_id']

            # Check if all required fields are present in the request body
            for field in required_fields:
                if field not in data:
                    return jsonify({"error": f"Missing required field: {field}"}), 400
                
            date_in_month = get_month(data['date'])
            project_id = get_project_name(data['project_name_id']).id

            # Create new test execution status from the provided data
            new_status = Test_execution_status(
                months=date_in_month,
                date=data['date'],
                total_execution=data['total_execution'],
                tc_execution=data['tc_execution'],
                pass_count=data['pass_count'],
                fail_count=data['fail_count'],
                no_run=data['no_run'],
                blocked=data['blocked'],
                project_name_id=project_id,
                user_id=int(get_jwt_identity())
            )

            # Add the new status to the database
            db.session.add(new_status)
            db.session.commit()

            return jsonify(new_status.to_dict()), 201  # Return created status with a 201 status

    # API endpoint to handle PUT and DELETE for '/test_execution_status/<int:id>'
    @app.route('/test_execution_status/<int:id>', methods=['PUT', 'DELETE'])
    @jwt_required()
    def update_or_delete_test_execution_status(id):
        # Get the status by ID
        status = Test_execution_status.query.get_or_404(id)

        if request.method == 'PUT':
            # If the method is PUT, update the test execution status
            data = request.json

            # Required fields for PUT request
            required_fields = ['months', 'date', 'total_execution', 'tc_execution', 'pass_count', 'fail_count', 'no_run',   'blocked', 'project_name_id']

            # Check if all required fields are present in the request body
            for field in required_fields:
                if field not in data:
                    return jsonify({"error": f"Missing required field: {field}"}), 400
            
            date_in_month = get_month(data['date'])
            project_id = get_project_name(data['project_name_id']).id

            # Update the status fields
            status.months = date_in_month
            status.date = data['date']
            status.total_execution = data['total_execution']
            status.tc_execution = data['tc_execution']
            status.pass_count = data['pass_count']
            status.fail_count = data['fail_count']
            status.no_run = data['no_run']
            status.blocked = data['blocked']
            status.project_name_id = project_id
            status.user_id = int(get_jwt_identity())

            # Commit changes to the database
            db.session.commit()
            return jsonify(status.to_dict())

        elif request.method == 'DELETE':
            # If the method is DELETE, remove the status
            db.session.delete(status)
            db.session.commit()
            return '', 204  # Return an empty response after successful deletion
        

# for form 3 in total defect status table
    @app.route('/total_defect_status', methods=['GET', 'POST'])
    @jwt_required()
    def manage_total_defect_status():
        if request.method == 'GET':
            # Handle GET request: Fetch all total defect statuses
            total_defects = Total_Defect_Status.query.all()
            return jsonify([defect.to_dict() for defect in total_defects])

        elif request.method == 'POST':
            # Handle POST request: Create a new total defect status
            data = request.json

            # Required fields for POST request
            required_fields = ['months', 'date', 'total_defect', 'defect_closed', 'open_defect', 'critical', 'high',    'medium', 'low', 'project_name_id']

            # Check if all required fields are present in the request body
            for field in required_fields:
                if field not in data:
                    return jsonify({"error": f"Missing required field: {field}"}), 400
                
            date_in_month = get_month(data['date'])
            project_id = get_project_name(data['project_name_id']).id

            # Create new total defect status from the provided data
            new_defect_status = Total_Defect_Status(
                months=date_in_month,
                date=data['date'],
                total_defect=data['total_defect'],
                defect_closed=data['defect_closed'],
                open_defect=data['open_defect'],
                critical=data['critical'],
                high=data['high'],
                medium=data['medium'],
                low=data['low'],
                project_name_id=project_id,
                user_id=int(get_jwt_identity())
            )

            # Add the new defect status to the database
            db.session.add(new_defect_status)
            db.session.commit()

            return jsonify(new_defect_status.to_dict()), 201  # Return created status with a 201 status

    # API endpoint to handle PUT and DELETE for '/total_defect_status/<int:id>'
    @app.route('/total_defect_status/<int:id>', methods=['PUT', 'DELETE'])
    @jwt_required()
    def update_or_delete_total_defect_status(id):
        # Get the status by ID
        defect_status = Total_Defect_Status.query.get_or_404(id)

        if request.method == 'PUT':
            # If the method is PUT, update the total defect status
            data = request.json

            # Required fields for PUT request
            required_fields = ['months', 'date', 'total_defect', 'defect_closed', 'open_defect', 'critical', 'high',    'medium', 'low', 'project_name_id']

            # Check if all required fields are present in the request body
            for field in required_fields:
                if field not in data:
                    return jsonify({"error": f"Missing required field: {field}"}), 400
                
            date_in_month = get_month(data['date'])
            project_id = get_project_name(data['project_name_id']).id

            # Update the defect status fields
            defect_status.months = date_in_month
            defect_status.date = data['date']
            defect_status.total_defect = data['total_defect']
            defect_status.defect_closed = data['defect_closed']
            defect_status.open_defect = data['open_defect']
            defect_status.critical = data['critical']
            defect_status.high = data['high']
            defect_status.medium = data['medium']
            defect_status.low = data['low']
            defect_status.project_name_id = project_id
            defect_status.user_id = int(get_jwt_identity())

            # Commit changes to the database
            db.session.commit()
            return jsonify(defect_status.to_dict())

        elif request.method == 'DELETE':
            # If the method is DELETE, remove the defect status
            db.session.delete(defect_status)
            db.session.commit()
            return '', 204  # Return an empty response after successful deletion
        

#for form 4 in bugs table

    @app.route('/build_status', methods=['GET', 'POST'])
    @jwt_required()
    def manage_build_status():
        if request.method == 'GET':
            # Handle GET request: Fetch all build statuses
            build_statuses = BuildStatus.query.all()
            return jsonify([status.to_dict() for status in build_statuses])

        elif request.method == 'POST':
            # Handle POST request: Create a new build status
            data = request.json

            # Required fields for POST request
            required_fields = ['month', 'date', 'total_build_received', 'builds_accepted', 'builds_rejected',   'project_name_id']

            # Check if all required fields are present in the request body
            for field in required_fields:
                if field not in data:
                    return jsonify({"error": f"Missing required field: {field}"}), 400

            date_in_month = get_month(data['date'])
            project_id = get_project_name(data['project_name_id'])

            # Create new build status from the provided data
            new_build_status = BuildStatus(
                month=date_in_month,
                date=data['date'],
                total_build_received=data['total_build_received'],
                builds_accepted=data['builds_accepted'],
                builds_rejected=data['builds_rejected'],
                project_name_id=project_id.id,
                user_id=int(get_jwt_identity())
            )

            # Add the new build status to the database
            db.session.add(new_build_status)
            db.session.commit()

            return jsonify(new_build_status.to_dict()), 201  # Return created status with a 201 status

    # API endpoint to handle PUT and DELETE for '/build_status/<int:id>'
    @app.route('/build_status/<int:id>', methods=['PUT', 'DELETE'])
    @jwt_required()
    def update_or_delete_build_status(id):
        # Get the build status by ID
        build_status = BuildStatus.query.get_or_404(id)

        if request.method == 'PUT':
            # If the method is PUT, update the build status
            data = request.json

            # Required fields for PUT request
            required_fields = ['month', 'date', 'total_build_received', 'builds_accepted', 'builds_rejected',   'project_name_id']

            # Check if all required fields are present in the request body
            for field in required_fields:
                if field not in data:
                    return jsonify({"error": f"Missing required field: {field}"}), 400
            
            date_in_month = get_month(data['date'])
            project_id = get_project_name(data['project_name_id']).id

            # Update the build status fields
            build_status.month = date_in_month
            build_status.date = data['date']
            build_status.total_build_received = data['total_build_received']
            build_status.builds_accepted = data['builds_accepted']
            build_status.builds_rejected = data['builds_rejected']
            build_status.project_name_id = project_id
            build_status.user_id = int(get_jwt_identity())

            # Commit changes to the database
            db.session.commit()
            return jsonify(build_status.to_dict())

        elif request.method == 'DELETE':
            # If the method is DELETE, remove the build status
            db.session.delete(build_status)
            db.session.commit()
            return '', 204  # Return an empty response after successful deletion


#for form 5 in bugs table

    @app.route('/defect_accepted_rejected', methods=['GET', 'POST'])
    @jwt_required()
    def manage_defect_accepted_rejected():
        if request.method == 'GET':
            # Handle GET request: Fetch all defect accepted/rejected records
            defect_records = DefectAcceptedRejected.query.all()
            return jsonify([record.to_dict() for record in defect_records])

        elif request.method == 'POST':
            # Handle POST request: Create a new defect accepted/rejected record
            data = request.json

            # Required fields for POST request
            required_fields = ['month', 'date', 'total_defects', 'dev_team_accepted', 'dev_team_rejected', 'project_name_id']

            # Check if all required fields are present in the request body
            for field in required_fields:
                if field not in data:
                    return jsonify({"error": f"Missing required field: {field}"}), 400
            
            date_in_month = get_month(data['date'])
            project_id = get_project_name(data['project_name_id']).id

            # Create new defect accepted/rejected record from the provided data
            new_defect_record = DefectAcceptedRejected(
                month=date_in_month,
                date=data['date'],
                total_defects=data['total_defects'],
                dev_team_accepted=data['dev_team_accepted'],
                dev_team_rejected=data['dev_team_rejected'],
                project_name_id=project_id,
                user_id=int(get_jwt_identity())
            )

            # Add the new defect accepted/rejected record to the database
            db.session.add(new_defect_record)
            db.session.commit()

            return jsonify(new_defect_record.to_dict()), 201  # Return created record with a 201 status

    # API endpoint to handle PUT and DELETE for '/defect_accepted_rejected/<int:id>'
    @app.route('/defect_accepted_rejected/<int:id>', methods=['PUT', 'DELETE'])
    @jwt_required()
    def update_or_delete_defect_accepted_rejected(id):
        # Get the defect accepted/rejected record by ID
        defect_record = DefectAcceptedRejected.query.get_or_404(id)

        if request.method == 'PUT':
            # If the method is PUT, update the defect accepted/rejected record
            data = request.json

            # Required fields for PUT request
            required_fields = ['month', 'date', 'total_defects', 'dev_team_accepted', 'dev_team_rejected', 'project_name_id']

            # Check if all required fields are present in the request body
            for field in required_fields:
                if field not in data:
                    return jsonify({"error": f"Missing required field: {field}"}), 400
                
            date_in_month = get_month(data['date'])
            project_id = get_project_name(data['project_name_id']).id

            # Update the defect accepted/rejected record fields
            defect_record.month = date_in_month
            defect_record.date = data['date']
            defect_record.total_defects = data['total_defects']
            defect_record.dev_team_accepted = data['dev_team_accepted']
            defect_record.dev_team_rejected = data['dev_team_rejected']
            defect_record.project_name_id = project_id
            defect_record.user_id = int(get_jwt_identity())

            # Commit changes to the database
            db.session.commit()
            return jsonify(defect_record.to_dict())

        elif request.method == 'DELETE':
            # If the method is DELETE, remove the defect accepted/rejected record
            db.session.delete(defect_record)
            db.session.commit()
            return '', 204  # Return an empty response after successful deletion
        

# for 6 in bugs table

    @app.route('/test_case_creation_status', methods=['GET', 'POST'])
    @jwt_required()
    def manage_test_case_creation_status():
        if request.method == 'GET':
            # Handle GET request: Fetch all test case creation status records
            test_case_records = TestCaseCreationStatus.query.all()
            return jsonify([record.to_dict() for record in test_case_records])

        elif request.method == 'POST':
            # Handle POST request: Create a new test case creation status record
            data = request.json

            # Required fields for POST request
            required_fields = ['month', 'date', 'total_test_case_created', 'test_case_approved', 'test_case_rejected',  'project_name_id']

            # Check if all required fields are present in the request body
            for field in required_fields:
                if field not in data:
                    return jsonify({"error": f"Missing required field: {field}"}), 400
                
            
            date_in_month = get_month(data['date'])
            project_id = get_project_name(data['project_name_id']).id

            # Create new test case creation status record from the provided data
            new_test_case_record = TestCaseCreationStatus(
                month=date_in_month,
                date=data['date'],
                total_test_case_created=data['total_test_case_created'],
                test_case_approved=data['test_case_approved'],
                test_case_rejected=data['test_case_rejected'],
                project_name_id=project_id,
                user_id=int(get_jwt_identity())
            )

            # Add the new test case creation status record to the database
            db.session.add(new_test_case_record)
            db.session.commit()

            return jsonify(new_test_case_record.to_dict()), 201  # Return created record with a 201 status

    # API endpoint to handle PUT and DELETE for '/test_case_creation_status/<int:id>'
    @app.route('/test_case_creation_status/<int:id>', methods=['PUT', 'DELETE'])
    @jwt_required()
    def update_or_delete_test_case_creation_status(id):
        # Get the test case creation status record by ID
        test_case_record = TestCaseCreationStatus.query.get_or_404(id)

        if request.method == 'PUT':
            # If the method is PUT, update the test case creation status record
            data = request.json

            # Required fields for PUT request
            required_fields = ['month', 'date', 'total_test_case_created', 'test_case_approved', 'test_case_rejected',  'project_name_id']

            # Check if all required fields are present in the request body
            for field in required_fields:
                if field not in data:
                    return jsonify({"error": f"Missing required field: {field}"}), 400

            date_in_month = get_month(data['date'])
            project_id = get_project_name(data['project_name_id']).id

            # Update the test case creation status record fields
            test_case_record.month = date_in_month
            test_case_record.date = data['date']
            test_case_record.total_test_case_created = data['total_test_case_created']
            test_case_record.test_case_approved = data['test_case_approved']
            test_case_record.test_case_rejected = data['test_case_rejected']
            test_case_record.project_name_id = project_id
            test_case_record.user_id = int(get_jwt_identity())

            # Commit changes to the database
            db.session.commit()
            return jsonify(test_case_record.to_dict())

        elif request.method == 'DELETE':
            # If the method is DELETE, remove the test case creation status record
            db.session.delete(test_case_record)
            db.session.commit()
            return '', 204  # Return an empty response after successful deletion