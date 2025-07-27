# Vercel entry point for StudySprint - Full Functionality
import os
import sys
from flask import Flask

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Database and environment setup
database_url = os.environ.get('DATABASE_URL')
secret_key = os.environ.get('SECRET_KEY', 'fallback-secret-key')

if database_url:
    try:
        # Import the full StudySprint app
        from app import app, db
        print("✅ Full StudySprint app imported successfully!")
        
        # Initialize database in serverless context
        with app.app_context():
            try:
                db.create_all()
                print("✅ Database tables initialized")
            except Exception as db_error:
                print(f"⚠️  Database table creation warning: {db_error}")
        
        print("🚀 StudySprint fully loaded with all features!")
        
    except Exception as import_error:
        print(f"❌ Import error: {import_error}")
        # Fallback to minimal app
        app = Flask(__name__)
        
        @app.route('/')
        def error_page():
            return f"""
            <h1>🚨 StudySprint Import Error</h1>
            <p><strong>Database connected, but app import failed:</strong></p>
            <p><code>{str(import_error)}</code></p>
            <p><a href="/health">Check Health Status</a></p>
            """
        
        @app.route('/health')
        def health():
            return {
                "status": "database_ok_import_failed",
                "database_url_set": True,
                "import_error": str(import_error)
            }

else:
    # No database URL - show config instructions
    app = Flask(__name__)
    
    @app.route('/')
    def config_needed():
        return """
        <h1>🔧 StudySprint Configuration Required</h1>
        <p>Please set DATABASE_URL environment variable in Vercel.</p>
        <p>Use the Supabase Transaction Pooler connection string.</p>
        """
    
    @app.route('/health')
    def health():
        return {
            "status": "needs_database_config",
            "database_url_set": False
        } 