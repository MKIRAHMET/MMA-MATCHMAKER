from app import app  # Import your app from the main app file
from extension import db
from models import User, Fighter, Matchup, Fight  # Import all models

# Create the database and tables
with app.app_context():
    db.create_all()
    print("Database and tables have been created successfully!")