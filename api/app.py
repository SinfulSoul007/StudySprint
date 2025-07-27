# Vercel entry point for StudySprint
import os
import sys
from flask import Flask

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Check if DATABASE_URL is set
database_url = os.environ.get('DATABASE_URL')
secret_key = os.environ.get('SECRET_KEY')

if not database_url:
    # Create error app for missing environment variables
    app = Flask(__name__)
    
    @app.route('/')
    def config_error():
        return f"""
        <h1>🔧 StudySprint Configuration Required</h1>
        <p><strong>❌ Missing Environment Variables</strong></p>
        <p>Please set these in your Vercel Dashboard:</p>
        <ul>
            <li><strong>DATABASE_URL:</strong> postgresql://postgres:studysprint123!@db.kfstzenkybnceicsjimu.supabase.co:5432/postgres</li>
            <li><strong>SECRET_KEY:</strong> studysprint-production-secret-2024</li>
        </ul>
        <p><em>DATABASE_URL exists: {bool(database_url)}</em></p>
        <p><em>SECRET_KEY exists: {bool(secret_key)}</em></p>
        <hr>
        <p>After setting environment variables, redeploy your app!</p>
        """
    
    @app.route('/debug')
    def debug():
        return {
            "database_url_exists": bool(database_url),
            "secret_key_exists": bool(secret_key),
            "env_vars": list(os.environ.keys())
        }

else:
    # Environment variables exist, try to import the full app
    try:
        from app import app
        print("✅ StudySprint app loaded successfully with database!")
    except Exception as e:
        # Create error app showing import failure
        app = Flask(__name__)
        
        @app.route('/')
        def import_error():
            return f"""
            <h1>🚨 StudySprint Import Error</h1>
            <p><strong>Error:</strong> {str(e)}</p>
            <p>Environment variables are set correctly, but app import failed.</p>
            <a href="/debug">View Debug Info</a>
            """
        
        @app.route('/debug')
        def debug():
            return {
                "error": str(e),
                "database_url_prefix": database_url[:30] + "..." if database_url else None,
                "secret_key_set": bool(secret_key)
            } 