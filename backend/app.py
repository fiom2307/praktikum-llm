from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv

load_dotenv()

from routes import register_routes
from database import Base, engine
import models

def create_app():
    app = Flask(__name__)

    CORS(
        app,
        resources={
            r"/*": {
                "origins": [
                    "http://localhost:3000",
                    "http://127.0.0.1:3000",
                    "http://localhost:3001",
                    "http://127.0.0.1:3001",
                    "http://localhost:3002",
                    "http://127.0.0.1:3002",
                    "https://praktikum-llm-1.onrender.com",
                ]
            }
        },
        supports_credentials=True,
        allow_headers=["Content-Type", "Authorization"],
        methods=["GET", "POST", "OPTIONS"],
    )

    Base.metadata.create_all(bind=engine)
    register_routes(app)
    return app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)