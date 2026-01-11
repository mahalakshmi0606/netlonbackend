import os
from flask import Flask, jsonify, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from config import Config

# Initialize extensions
db = SQLAlchemy()
migrate = Migrate()
# jwt = JWTManager()  # REMOVE JWT

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    # jwt.init_app(app)  # REMOVE JWT

    # Enable CORS
    CORS(app, resources={
        r"/api/*": {
            "origins": "*",
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization"]
        },
        r"/login": {"origins": "*"},
        r"/register": {"origins": "*"}
    })

    # Import models (so they’re registered properly for migrations)
    with app.app_context():
        from app.models import login  # add more models if needed

    # Register Blueprints
    from app.routes import login_bp
    from app.routes import quotations_bp
    app.register_blueprint(login_bp, url_prefix='/')
    app.register_blueprint(quotations_bp, url_prefix='/api/')


    # Serve uploaded files
    @app.route('/uploads/<path:filename>')
    def serve_uploaded_file(filename):
        upload_folder = os.path.join(os.getcwd(), 'uploads')
        return send_from_directory(upload_folder, filename)

    # Health check route
    @app.route('/')
    def health_check():
        return jsonify({'status': 'healthy'})

    return app
