from routers.billable_details_route import billable_details_route
from routers.project_details_route import project_details_route
from routers.test_details_route import test_details_route
from routers.router import register_router


def all_router(app):
    billable_details_route(app)
    project_details_route(app)
    test_details_route(app)
    register_router(app)
