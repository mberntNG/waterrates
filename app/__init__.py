from flask import Flask
from .extensions import db
from .routes import main as main_blueprint

def create_app():
    app = Flask(__name__)

    # Configuration settings (adjust as necessary)
    app.config['SECRET_KEY'] = 'your-secret-key'  # Set a secret key for session management
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///water_rates.sqlite'  # SQLite database URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Disable modification tracking

    # Initialize extensions
    db.init_app(app)

    # Register blueprints
    app.register_blueprint(main_blueprint)

    return app
