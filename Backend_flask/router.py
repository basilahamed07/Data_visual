from flask import Flask, request, jsonify
from flask_jwt_extended import jwt_required, create_access_token
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, Users, Project_name, Project_details, Testers, New_defects, Test_execution_status, Total_Defect_Status, BuildStatus, DefectAcceptedRejected, TestCaseCreationStatus

def register_router(app):
    # Register User Routes (Already in your example)
    
    # User Registration
    @app.route('/register', methods=['POST'])
    def register_user():
        data = request.json
        if 'username' not in data or 'password' not in data:
            return jsonify({'error': 'Username and password required'}), 400
        
        if Users.query.filter_by(username=data['username']).first():
            return jsonify({'error': 'User already exists'}), 400
        
        hashed_password = generate_password_hash(data['password'])
        new_user = Users(username=data['username'], password=hashed_password)
        
        try:
            db.session.add(new_user)
            db.session.commit()
            return jsonify({'message': 'User registered successfully'}), 201
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500

    # User Login
    @app.route('/login', methods=['POST'])
    def login_user():
        data = request.json
        if 'username' not in data or 'password' not in data:
            return jsonify({'error': 'Username and password required'}), 400
        
        user = Users.query.filter_by(username=data['username']).first()
        if not user or not check_password_hash(user.password, data['password']):
            return jsonify({'error': 'Invalid credentials'}), 401
        
        access_token = create_access_token(identity=user.id)
        
        return jsonify({
            'message': 'Login successful',
            'access_token': access_token,
            'user': {'username': user.username, 'userId': user.id}
        }), 200


    # Project Name Routes
    @app.route('/projects', methods=['GET'])
    @jwt_required()
    def get_projects():
        projects = Project_name.query.all()
        return jsonify([project.to_dict() for project in projects])

    @app.route('/projects', methods=['POST'])
    @jwt_required()
    def add_project():
        data = request.get_json()
        new_project = Project_name(project_name=data['project_name'])
        db.session.add(new_project)
        db.session.commit()
        return jsonify(new_project.to_dict()), 201


    # Project Details Routes
    @app.route('/project_details', methods=['GET'])
    @jwt_required()
    def get_project_details():
        project_details = Project_details.query.all()
        return jsonify([detail.to_dict() for detail in project_details])

    @app.route('/project_details', methods=['POST'])
    @jwt_required()
    def add_project_details():
        data = request.get_json()
        new_detail = Project_details(
            project_name_id=data['project_name_id'],
            RAG=data['RAG'],
            tester_count=data['tester_count'],
            billable=data['billable'],
            nonbillable=data['nonbillable'],
            billing_type=data['billing_type'],
            automation=data['automation'],
            ai_used=data['ai_used'],
            RAG_details=data['RAG_details']
        )
        db.session.add(new_detail)
        db.session.commit()
        return jsonify(new_detail.to_dict()), 201


    # Testers Routes
    @app.route('/testers', methods=['GET'])
    @jwt_required()
    def get_testers():
        testers = Testers.query.all()
        return jsonify([tester.to_dict() for tester in testers])

    @app.route('/testers', methods=['POST'])
    @jwt_required()
    def add_tester():
        data = request.get_json()
        new_tester = Testers(
            tester_name=data['tester_name'],
            billable=data['billable'],
            project_name_id=data['project_name_id']
        )
        db.session.add(new_tester)
        db.session.commit()
        return jsonify(new_tester.to_dict()), 201


    # New Defects Routes
    @app.route('/new_defects', methods=['GET'])
    @jwt_required()
    def get_new_defects():
        defects = New_defects.query.all()
        return jsonify([defect.to_dict() for defect in defects])

    @app.route('/new_defects', methods=['POST'])
    @jwt_required()
    def add_new_defect():
        data = request.get_json()
        new_defect = New_defects(
            date=data['date'],
            months=data['months'],
            regression_defect=data['regression_defect'],
            functional_defect=data['functional_defect'],
            defect_reopened=data['defect_reopened'],
            uat_defect=data['uat_defect'],
            project_name_id=data['project_name_id']
        )
        db.session.add(new_defect)
        db.session.commit()
        return jsonify(new_defect.to_dict()), 201


    # Test Execution Status Routes
    @app.route('/test_execution_status', methods=['GET'])
    @jwt_required()
    def get_test_execution_status():
        status = Test_execution_status.query.all()
        return jsonify([status.to_dict() for status in status])

    @app.route('/test_execution_status', methods=['POST'])
    @jwt_required()
    def add_test_execution_status():
        data = request.get_json()
        new_status = Test_execution_status(
            months=data['months'],
            date=data['date'],
            total_execution=data['total_execution'],
            tc_execution=data['tc_execution'],
            pass_count=data['pass_count'],
            fail_count=data['fail_count'],
            no_run=data['no_run'],
            blocked=data['blocked'],
            project_name_id=data['project_name_id']
        )
        db.session.add(new_status)
        db.session.commit()
        return jsonify(new_status.to_dict()), 201


    # Total Defect Status Routes
    @app.route('/total_defect_status', methods=['GET'])
    @jwt_required()
    def get_total_defect_status():
        status = Total_Defect_Status.query.all()
        return jsonify([status.to_dict() for status in status])

    @app.route('/total_defect_status', methods=['POST'])
    @jwt_required()
    def add_total_defect_status():
        data = request.get_json()
        new_status = Total_Defect_Status(
            months=data['months'],
            date=data['date'],
            total_defect=data['total_defect'],
            defect_closed=data['defect_closed'],
            open_defect=data['open_defect'],
            critical=data['critical'],
            high=data['high'],
            medium=data['medium'],
            low=data['low'],
            project_name_id=data['project_name_id']
        )
        db.session.add(new_status)
        db.session.commit()
        return jsonify(new_status.to_dict()), 201


    # Build Status Routes
    @app.route('/build_status', methods=['GET'])
    @jwt_required()
    def get_build_status():
        status = BuildStatus.query.all()
        return jsonify([status.to_dict() for status in status])

    @app.route('/build_status', methods=['POST'])
    @jwt_required()
    def add_build_status():
        data = request.get_json()
        new_status = BuildStatus(
            month=data['month'],
            date=data['date'],
            total_build_received=data['total_build_received'],
            builds_accepted=data['builds_accepted'],
            builds_rejected=data['builds_rejected'],
            project_name_id=data['project_name_id']
        )
        db.session.add(new_status)
        db.session.commit()
        return jsonify(new_status.to_dict()), 201


    # Defect Accepted vs Rejected Routes
    @app.route('/defect_accepted_rejected', methods=['GET'])
    @jwt_required()
    def get_defect_accepted_rejected():
        status = DefectAcceptedRejected.query.all()
        return jsonify([status.to_dict() for status in status])

    @app.route('/defect_accepted_rejected', methods=['POST'])
    @jwt_required()
    def add_defect_accepted_rejected():
        data = request.get_json()
        new_status = DefectAcceptedRejected(
            month=data['month'],
            date=data['date'],
            total_defects=data['total_defects'],
            dev_team_accepted=data['dev_team_accepted'],
            dev_team_rejected=data['dev_team_rejected'],
            project_name_id=data['project_name_id']
        )
        db.session.add(new_status)
        db.session.commit()
        return jsonify(new_status.to_dict()), 201


    # Test Case Creation Status Routes
    @app.route('/test_case_creation_status', methods=['GET'])
    @jwt_required()
    def get_test_case_creation_status():
        status = TestCaseCreationStatus.query.all()
        return jsonify([status.to_dict() for status in status])

    @app.route('/test_case_creation_status', methods=['POST'])
    @jwt_required()
    def add_test_case_creation_status():
        data = request.get_json()
        new_status = TestCaseCreationStatus(
            month=data['month'],
            date=data['date'],
            total_test_case_created=data['total_test_case_created'],
            test_case_approved=data['test_case_approved'],
            test_case_rejected=data['test_case_rejected'],
            project_name_id=data['project_name_id']
        )
        db.session.add(new_status)
        db.session.commit()
        return jsonify(new_status.to_dict()), 201
