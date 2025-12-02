from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv

load_dotenv()

from routes import register_routes
from database import Base, engine
import models

def create_app():
    app = Flask(__name__)
    CORS(app, resources={r"/*": {"origins": "*"}})

    Base.metadata.create_all(bind=engine)

    register_routes(app)
    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
