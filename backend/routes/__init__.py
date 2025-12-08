from .auth_route import auth_routes
from .writing_route import writing_routes
from .reading_route import reading_routes
from .vocabulary_route import vocabulary_routes
from .pizza_count_route import pizza_count_routes
from .flashcard_route import flashcard_routes
from routes.shop_route import shop_bp

def register_routes(app):
    app.register_blueprint(auth_routes)
    app.register_blueprint(writing_routes)
    app.register_blueprint(reading_routes)
    app.register_blueprint(vocabulary_routes)
    app.register_blueprint(pizza_count_routes)
    app.register_blueprint(flashcard_routes)
    app.register_blueprint(shop_bp, url_prefix='/api')