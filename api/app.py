# Vercel entry point for StudySprint
import sys
import os

# Add parent directory to path so we can import from root
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import the Flask app and database
from app import app, db

# Initialize database tables in serverless environment
try:
    with app.app_context():
        db.create_all()
except Exception as e:
    print(f"Database initialization error: {e}") 