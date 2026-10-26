# Creates the Flask application and connects its components.

from flask import Flask
from flask_cors import CORS
from config import Config
from app.database import init_db


def create_app():
    """Build and configure the Flask app. Called once from run.py."""
    app = Flask(__name__)
    app.config.from_object(Config)

    # Allow the Wix site (a different domain) to send requests to this API
    CORS(app)

    # Make sure the "user" table exists before the app starts handling requests
    try:
        init_db()
    except Exception as e:
        print(f"[app] Failed to set up the database: {e}")

    # Register the routes defined in routes.py
    try:
        from app.routes import main_bp
        app.register_blueprint(main_bp)
    except Exception as e:
        print(f"[app] Failed to register routes: {e}")

    return app
