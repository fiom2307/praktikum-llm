from .auth_route import auth_routes
from .writing_route import writing_routes
from .reading_route import reading_routes
from .vocabulary_route import vocabulary_routes
from .pizza_count_route import pizza_count_routes
from .flashcard_route import flashcard_routes
from routes.shop_route import shop_bp
from .user_route import user_routes
from .form_settings_route import form_settings_routes
from routes.city_route import city_routes
from .user_city_progress_route import user_city_progress_routes
from .admin_route import admin_routes

def register_routes(app):
    app.register_blueprint(auth_routes)
    app.register_blueprint(writing_routes)
    app.register_blueprint(reading_routes)
    app.register_blueprint(vocabulary_routes)
    app.register_blueprint(pizza_count_routes)
    app.register_blueprint(flashcard_routes)
    app.register_blueprint(shop_bp, url_prefix='/api')
    app.register_blueprint(user_routes)
    app.register_blueprint(form_settings_routes)
    app.register_blueprint(city_routes)
    app.register_blueprint(user_city_progress_routes)
    app.register_blueprint(admin_routes)
