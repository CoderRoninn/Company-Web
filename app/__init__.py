# Creates the Flask application and connects its components.

from flask import Flask
from config import Config
from app.database import init_db


def create_app():
    """Build and configure the Flask app. Called once from run.py."""
    app = Flask(__name__)
    app.config.from_object(Config)

    # Make sure the "user" table exists before the app starts handling requests
    init_db()

    # Register the routes defined in routes.py
    from app.routes import main_bp
    app.register_blueprint(main_bp)

    return app
