from flask import Flask, send_from_directory
from flask_cors import CORS
from dotenv import load_dotenv
import os

load_dotenv()

from routes import register_routes
from database import Base, engine
import models
from seeds.seed_all import seed_all

def create_app():
    app = Flask(
        __name__,
        static_folder="dist",
        static_url_path="")

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

    if os.getenv("SYNC_SEEDS", "false").lower() == "true":
        seed_all()

    register_routes(app)

    @app.route("/", defaults={"path": ""})
    @app.route("/<path:path>")
    def serve_react(path):
        if path != "" and os.path.exists(os.path.join(app.static_folder, path)):
            return send_from_directory(app.static_folder, path)
        return send_from_directory(app.static_folder, "index.html")

    return app

app = create_app()

if __name__ == "__main__":
    app.run(debug=False)