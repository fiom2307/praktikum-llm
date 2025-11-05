from .auth_route import auth_routes
from .text_route import text_routes

def register_routes(app):
    app.register_blueprint(auth_routes)
    app.register_blueprint(text_routes)