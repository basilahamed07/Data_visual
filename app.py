import dash
from dash import dcc, html, Input, Output, State
from dash.exceptions import PreventUpdate
from sqlalchemy import create_engine
from Data_visual.models import TestCase, User, session
from Data_visual.db_config import DATABASE_URL
from datetime import datetime

# Create Dash app
app = dash.Dash(__name__)

# Create the engine and session

def get_all_user():
    # Fetch the latest users from the database
    full_users = session.query(User.email).all()
    return [{'label': email, 'value': email} for email, in full_users]

# Layout of the form with user registration option
app.layout = html.Div([
    
    html.Div([
        html.H1("Test Case Form", style={'textAlign': 'center', 'marginBottom': '40px', 'color': '#4CAF50'}),

        # User Registration Section
        html.Div([
            html.H3("User Registration", style={'textAlign': 'center', 'marginBottom': '20px', 'color': '#4CAF50'}),
            html.Div([
                html.Label("Email", style={'fontWeight': 'bold'}),
                dcc.Input(
                    id='register_email',
                    type='email',
                    placeholder="Enter your email",
                    style={'width': '60%', 'marginBottom': '20px', 'borderRadius': '5px', 'padding': '10px'}
                ),
            ], style={'marginBottom': '20px'}),

            html.Div([
                html.Label("Password", style={'fontWeight': 'bold'}),
                dcc.Input(
                    id='register_password',
                    type='password',
                    placeholder="Enter your password",
                    style={'width': '60%', 'marginBottom': '20px', 'borderRadius': '5px', 'padding': '10px'}
                ),
            ], style={'marginBottom': '20px'}),

            html.Div([
                html.Label("Role", style={'fontWeight': 'bold'}),
                dcc.Dropdown(
                    id='register_role',
                    options=[
                        {'label': 'Admin', 'value': 'Admin'},
                        {'label': 'User', 'value': 'User'}
                    ],
                    placeholder="Select your role",
                    style={'width': '60%', 'marginBottom': '20px', 'borderRadius': '5px', 'padding': '10px'}
                ),
            ], style={'marginBottom': '20px'}),

            html.Button("Register", id='register_button', n_clicks=0,
                        style={'backgroundColor': '#4CAF50', 'color': 'white', 'border': 'none',
                               'borderRadius': '5px', 'padding': '10px 20px', 'cursor': 'pointer',
                               'width': '60%', 'marginBottom': '30px'}),
            html.Div(id='registration_message', style={'textAlign': 'center', 'fontSize': '18px', 'fontWeight': 'bold'}),
        ], style={'marginBottom': '40px', 'border': '1px solid #ddd', 'borderRadius': '8px', 'backgroundColor': '#f9f9f9', 'padding': '20px'}),

        # Test Case Form
        html.Div([
            html.Label("User Email", style={'fontWeight': 'bold'}),
            dcc.Dropdown(
                id='user_email',
                options=get_all_user(),  # Initialize with the current users in the database
                placeholder="Select User Email",
                style={'width': '60%', 'marginBottom': '20px', 'borderRadius': '5px', 'padding': '10px'}
            ),
        ], style={'marginBottom': '30px'}),

        html.Div([
            html.Label("Test Case Summary", style={'fontWeight': 'bold'}),
            dcc.Textarea(
                id='test_case_summary',
                placeholder="Enter Test Case Summary",
                style={'width': '60%', 'height': 100, 'padding': '10px', 'borderRadius': '5px', 'border': '1px solid #ddd'}
            ),
        ], style={'marginBottom': '30px'}),

        html.Div([
            html.Label("Regression", style={'fontWeight': 'bold'}),
            dcc.Checklist(
                id='regression',
                options=[{'label': 'Regression', 'value': True}],
                value=[False],
                style={'marginBottom': '20px'}
            ),
        ], style={'marginBottom': '20px'}),

        html.Div([
            html.Label("New", style={'fontWeight': 'bold'}),
            dcc.Checklist(
                id='new',
                options=[{'label': 'New', 'value': True}],
                value=[False],
                style={'marginBottom': '20px'}
            ),
        ], style={'marginBottom': '20px'}),

        html.Div([
            html.Label("Reopen", style={'fontWeight': 'bold'}),
            dcc.Checklist(
                id='reopen',
                options=[{'label': 'Reopen', 'value': True}],
                value=[False],
                style={'marginBottom': '20px'}
            ),
        ], style={'marginBottom': '20px'}),

        html.Div([
            html.Label("UAT", style={'fontWeight': 'bold'}),
            dcc.Checklist(
                id='uat',
                options=[{'label': 'UAT', 'value': True}],
                value=[False],
                style={'marginBottom': '30px'}
            ),
        ], style={'marginBottom': '30px'}),

        html.Div([
            html.Button("Submit", id='submit_button', n_clicks=0,
                        style={'backgroundColor': '#4CAF50', 'color': 'white', 'border': 'none',
                               'borderRadius': '5px', 'padding': '10px 20px', 'cursor': 'pointer',
                               'width': '60%'}),
        ], style={'textAlign': 'center', 'marginBottom': '40px'}),

        html.Div(id='output_message', style={'textAlign': 'center', 'fontSize': '18px', 'fontWeight': 'bold'}),
    ], style={'width': '50%', 'margin': '0 auto', 'padding': '20px', 'border': '1px solid #ddd', 'borderRadius': '8px', 'backgroundColor': '#f9f9f9'}),

], style={'fontFamily': 'Arial, sans-serif'})

# Callback to handle user registration
@app.callback(
    Output('registration_message', 'children'),
    Input('register_button', 'n_clicks'),
    State('register_email', 'value'),
    State('register_password', 'value'),
    State('register_role', 'value')
)
def register_user(n_clicks, email, password, role):
    if n_clicks == 0:
        raise PreventUpdate

    if not email or not password or not role:
        return "Please fill in all the fields."

    # Check if the user already exists
    existing_user = session.query(User).filter_by(email=email).first()
    if existing_user:
        return "User already exists."

    # Create a new user and add to the session
    new_user = User(email=email, password=password, role=role, created_at=datetime.utcnow())
    session.add(new_user)
    session.commit()

    return f"User {email} registered successfully. You can now select your email in the Test Case Form."


# Callback to update user list in dropdown after registration
@app.callback(
    Output('user_email', 'options'),
    Input('register_button', 'n_clicks'),
    prevent_initial_call=False  # Allow callback to run when registering a new user
)
def update_user_dropdown(n_clicks):
    # When a user is registered, update the email dropdown
    return get_all_user()


# Callback to handle test case submission
@app.callback(
    Output('output_message', 'children'),
    Input('submit_button', 'n_clicks'),
    State('user_email', 'value'),
    State('test_case_summary', 'value'),
    State('regression', 'value'),
    State('new', 'value'),
    State('reopen', 'value'),
    State('uat', 'value')
)
def submit_test_case(n_clicks, user_email, summary, regression, new, reopen, uat):
    if n_clicks == 0:
        raise PreventUpdate

    # Validate inputs
    if not user_email or not summary:
        return "Please fill in all required fields."

    # Find user by email
    user = session.query(User).filter_by(email=user_email).first()
    if not user:
        return "User not found."

    # Create new TestCase object
    new_test_case = TestCase(
        TestCase_id=TestCase.generate_test_case_id(session),
        user_id=user.id,
        summary=summary,
        regression=bool(regression),
        new=bool(new),
        reopen=bool(reopen),
        uat=bool(uat),
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )

    # Add the new test case to the session and commit to the database
    session.add(new_test_case)
    session.commit()

    return f"Test Case '{new_test_case.TestCase_id}' added successfully."

if __name__ == '__main__':
    app.run_server(debug=True)
