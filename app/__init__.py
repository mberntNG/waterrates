from flask import Flask
from app.extensions import db
from app.routes import main as main_blueprint

def create_app():
    app = Flask(__name__)
    
    # Load the config from config.py
    app.config.from_object('config.Config')

    # Initialize extensions
    db.init_app(app)

    # Register blueprints
    app.register_blueprint(main_blueprint)

    return app
