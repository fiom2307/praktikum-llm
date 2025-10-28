from flask import Flask, jsonify
from flask_cors import CORS
from routes.login import login_routes

app = Flask(__name__)
CORS(app)
app.register_blueprint(login_routes)

if __name__ == "__main__":
    app.run(debug=True)