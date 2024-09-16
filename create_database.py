from app import create_app, db
from app.models import Entity, Rate, Block

def create_db():
    app = create_app()
    with app.app_context():
        # Create all tables
        db.create_all()
        print("Database and tables created successfully.")

if __name__ == "__main__":
    create_db()
