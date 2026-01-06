from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
import os

load_dotenv()

from routes import register_routes
from database import Base, engine
import models
from seeds.cities_seed import seed_cities

def create_app():
    app = Flask(__name__)

    CORS(app, resources={r"/*": {
        "origins": 
            ["http://localhost:3000", 
            "http://127.0.0.1:3000",
            "http://localhost:3001", 
            "http://127.0.0.1:3001",
            "http://localhost:3002",
            "http://127.0.0.1:3002"], # React frontend address
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"]
    }})

    Base.metadata.create_all(bind=engine)

    if os.getenv("SYNC_SEEDS", "false").lower() == "true":
        seed_cities()

    register_routes(app)
    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
