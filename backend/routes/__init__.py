from .auth_route import auth_routes
from .writing_route import writing_routes
from .reading_route import reading_routes
from .vocabulary_route import vocabulary_routes

def register_routes(app):
    app.register_blueprint(auth_routes)
    app.register_blueprint(writing_routes)
    app.register_blueprint(reading_routes)
    app.register_blueprint(vocabulary_routes)