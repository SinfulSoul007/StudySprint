# Vercel entry point for StudySprint
import sys
import os

print("Starting Vercel function initialization...")

try:
    # Add parent directory to path so we can import from root
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    print("Python path configured successfully")
    
    # Import the Flask app and database
    from app import app, db
    print("Flask app imported successfully")
    
    # Check environment variables
    database_url = os.environ.get('DATABASE_URL')
    secret_key = os.environ.get('SECRET_KEY')
    print(f"DATABASE_URL exists: {bool(database_url)}")
    print(f"SECRET_KEY exists: {bool(secret_key)}")
    
    if database_url:
        print(f"Database URL prefix: {database_url[:20]}...")
    
    # Initialize database tables in serverless environment
    try:
        with app.app_context():
            print("Creating database tables...")
            db.create_all()
            print("Database initialization successful")
    except Exception as db_error:
        print(f"Database initialization error: {db_error}")
        # Don't fail completely, let the app start without DB
    
    print("Vercel function initialization complete")
    
except Exception as init_error:
    print(f"Critical initialization error: {init_error}")
    # Create a minimal Flask app as fallback
    from flask import Flask
    app = Flask(__name__)
    
    @app.route('/')
    def error_page():
        return f"Initialization failed: {init_error}", 500 