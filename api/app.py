# Vercel entry point for StudySprint - Robust Error Handling
import os
import sys
from flask import Flask

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Check environment variables
database_url = os.environ.get('DATABASE_URL')
secret_key = os.environ.get('SECRET_KEY')

# Create Flask app
app = Flask(__name__)

if not database_url:
    # No database URL - show config page
    @app.route('/')
    def config_error():
        return f"""
        <h1>🔧 StudySprint Configuration Required</h1>
        <p><strong>❌ Missing DATABASE_URL</strong></p>
        <p>Please set DATABASE_URL in your Vercel Dashboard.</p>
        """
else:
    # Environment variables exist - try to load app with error handling
    try:
        # Test basic imports first
        print("Testing basic imports...")
        from models import db, User, Problem, Submission, Sprint
        print("✅ Models imported successfully")
        
        # Configure Flask app manually for serverless
        app.config["SQLALCHEMY_DATABASE_URI"] = database_url
        app.config["SECRET_KEY"] = secret_key or "fallback-secret-key"
        app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
        
        # Initialize database
        print("Initializing database...")
        db.init_app(app)
        
        # Test database connection
        with app.app_context():
            try:
                db.create_all()
                print("✅ Database initialized successfully")
                
                # Import routes after database is ready
                from app import app as main_app
                # Copy routes from main app
                for rule in main_app.url_map.iter_rules():
                    if rule.endpoint != 'static':
                        app.add_url_rule(
                            rule.rule, 
                            rule.endpoint, 
                            main_app.view_functions[rule.endpoint],
                            methods=rule.methods
                        )
                print("✅ Routes imported successfully")
                
            except Exception as db_error:
                print(f"❌ Database error: {db_error}")
                # Create error page for database issues
                @app.route('/')
                def db_error_page():
                    return f"""
                    <h1>🗄️ Database Connection Error</h1>
                    <p><strong>Error:</strong> {str(db_error)}</p>
                    <p><strong>Database URL:</strong> {database_url[:50]}...</p>
                    <p>Check if your Supabase database is active.</p>
                    <a href="/debug">Debug Info</a>
                    """
                
                @app.route('/debug')
                def debug():
                    return {
                        "database_error": str(db_error),
                        "database_url_set": bool(database_url),
                        "secret_key_set": bool(secret_key)
                    }
                
    except Exception as import_error:
        print(f"❌ Import error: {import_error}")
        # Create error page for import issues
        @app.route('/')
        def import_error_page():
            return f"""
            <h1>📦 Import Error</h1>
            <p><strong>Error:</strong> {str(import_error)}</p>
            <p>Failed to import StudySprint components.</p>
            <a href="/debug">Debug Info</a>
            """
        
        @app.route('/debug')
        def debug():
            return {
                "import_error": str(import_error),
                "python_path": sys.path,
                "current_dir": os.path.dirname(os.path.abspath(__file__))
            }

# Health check route that should always work
@app.route('/health')
def health():
    return {
        "status": "ok", 
        "database_url_set": bool(database_url),
        "secret_key_set": bool(secret_key)
    } 