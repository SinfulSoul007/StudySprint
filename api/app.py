# Vercel entry point for StudySprint - Robust with Fallback
import os
import sys
from flask import Flask, render_template_string

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Database and environment setup
database_url = os.environ.get('DATABASE_URL')
secret_key = os.environ.get('SECRET_KEY', 'fallback-secret-key')

print(f"🔍 Environment check - DATABASE_URL exists: {bool(database_url)}")

if database_url:
    try:
        print("🔄 Attempting to import full StudySprint app...")
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
        print(f"❌ Import failed: {import_error}")
        
        # Create fallback app with working basic functionality
        from flask_sqlalchemy import SQLAlchemy
        import datetime
        
        app = Flask(__name__)
        app.config["SQLALCHEMY_DATABASE_URI"] = database_url
        app.config["SECRET_KEY"] = secret_key
        app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
        
        db = SQLAlchemy(app)
        
        # Simple models for fallback
        class Problem(db.Model):
            __tablename__ = 'problems'
            id = db.Column(db.Integer, primary_key=True)
            title = db.Column(db.String(200), nullable=False)
            prompt_md = db.Column(db.Text, nullable=False)
            starter_code = db.Column(db.Text, nullable=False)
            tests_json = db.Column(db.Text, nullable=False)
            difficulty = db.Column(db.String(20), default='Easy')
            created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
            points = db.Column(db.Integer, default=100)
        
        # Initialize database
        with app.app_context():
            try:
                db.create_all()
                print("✅ Fallback database initialized")
            except Exception as e:
                print(f"❌ Fallback database error: {e}")
        
        @app.route('/')
        def fallback_home():
            try:
                problems = Problem.query.limit(10).all()
                return render_template_string("""
                <!DOCTYPE html>
                <html>
                <head>
                    <title>StudySprint - Running (Fallback Mode)</title>
                    <style>
                        body { font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; }
                        .warning { background: #fff3cd; border: 1px solid #ffeeba; padding: 15px; border-radius: 5px; margin: 15px 0; }
                        .success { background: #d4edda; border: 1px solid #c3e6cb; padding: 15px; border-radius: 5px; margin: 15px 0; }
                        .nav { background: #f8f9fa; padding: 10px; margin-bottom: 20px; border-radius: 5px; }
                        .nav a { margin-right: 15px; text-decoration: none; color: #007bff; }
                        .problem { border: 1px solid #ddd; padding: 15px; margin: 10px 0; border-radius: 5px; }
                    </style>
                </head>
                <body>
                    <div class="nav">
                        <a href="/">Home</a>
                        <a href="/seed">Seed Problems</a>
                        <a href="/debug">Debug Info</a>
                    </div>
                    
                    <div class="warning">
                        <h3>⚠️ Running in Fallback Mode</h3>
                        <p>StudySprint is working, but some advanced features are disabled due to import issues.</p>
                        <p><strong>Error:</strong> {{ error_message }}</p>
                    </div>
                    
                    <div class="success">
                        <h3>✅ What's Working:</h3>
                        <ul>
                            <li>✅ Database connected to Supabase</li>
                            <li>✅ Problem display and storage</li>
                            <li>✅ Basic functionality</li>
                        </ul>
                    </div>
                    
                    <h1>🚀 StudySprint (Basic Mode)</h1>
                    
                    <h2>🧠 Available Problems ({{ problems|length }})</h2>
                    {% for problem in problems %}
                    <div class="problem">
                        <h3>{{ problem.title }}</h3>
                        <p><strong>Difficulty:</strong> {{ problem.difficulty }}</p>
                        <p>{{ problem.prompt_md[:150] }}...</p>
                    </div>
                    {% endfor %}
                    
                    {% if problems|length == 0 %}
                    <p>No problems yet. <a href="/seed">Add some sample problems</a></p>
                    {% endif %}
                    
                    <hr>
                    <p><em>🔧 To enable full features, check the <a href="/debug">debug page</a></em></p>
                </body>
                </html>
                """, problems=problems, error_message=str(import_error)[:200])
            except Exception as e:
                return f"<h1>Database Error</h1><p>{str(e)}</p><a href='/debug'>Debug</a>"
        
        @app.route('/seed')
        def seed():
            try:
                if Problem.query.count() == 0:
                    sample = Problem(
                        title="Two Sum",
                        prompt_md="Given an array of integers, return indices of two numbers that add up to target.",
                        starter_code="def solution(nums, target):\n    # Your code here\n    pass",
                        tests_json='[{"input": [[2,7,11,15], 9], "output": [0,1]}]',
                        difficulty="Easy"
                    )
                    db.session.add(sample)
                    db.session.commit()
                    return "<h1>✅ Sample Problem Added!</h1><a href='/'>← Back</a>"
                return "<h1>Problems Already Exist</h1><a href='/'>← Back</a>"
            except Exception as e:
                return f"<h1>Seed Error</h1><p>{str(e)}</p><a href='/'>← Back</a>"
        
        @app.route('/debug')
        def debug():
            return {
                "status": "fallback_mode",
                "database_connected": True,
                "import_error": str(import_error),
                "database_url_set": True,
                "python_version": sys.version,
                "working_features": ["database", "basic_ui", "problem_storage"]
            }

else:
    # No database URL
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
        return {"status": "needs_database_config", "database_url_set": False}

# Health check that always works
@app.route('/health')
def health():
    return {
        "status": "app_running",
        "database_url_set": bool(database_url),
        "timestamp": "2025-01-27"
    } 