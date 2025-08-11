from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from .config import Config

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object(Config)

    # Enable CORS (for React frontend)
    CORS(app, 
         resources={r"/api/*": {"origins": "*"}},
         methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
         allow_headers=["Content-Type", "Authorization"],
         supports_credentials=True)

    # Initialize DB
    db.init_app(app)
    migrate.init_app(app, db)

    # Register routes
    from routes import api_bp
    app.register_blueprint(api_bp, url_prefix="/api")

    @app.route("/health", methods=["GET"])
    def health_check():
        return jsonify({"status": "ok"}), 200
    
    # Handle OPTIONS requests globally
    @app.before_request
    def handle_preflight():
        if request.method == "OPTIONS":
            response = jsonify()
            response.headers.add("Access-Control-Allow-Origin", "*")
            response.headers.add('Access-Control-Allow-Headers', "*")
            response.headers.add('Access-Control-Allow-Methods', "*")
            return response

    return app