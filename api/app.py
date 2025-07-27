# Vercel entry point for StudySprint - With Database Fallback
import os
from flask import Flask, render_template_string
from flask_sqlalchemy import SQLAlchemy
import datetime

# Create Flask app
app = Flask(__name__)

# Database Configuration
database_url = os.environ.get('DATABASE_URL')
secret_key = os.environ.get('SECRET_KEY', 'fallback-secret-key')

# Test database connection
database_connected = False
db_error_message = None

if database_url:
    app.config["SQLALCHEMY_DATABASE_URI"] = database_url
    app.config["SECRET_KEY"] = secret_key
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    
    try:
        # Initialize database
        db = SQLAlchemy(app)
        
        # Define models
        class User(db.Model):
            __tablename__ = 'users'
            id = db.Column(db.Integer, primary_key=True)
            username = db.Column(db.String(80), unique=True, nullable=False)
            pass_hash = db.Column(db.String(255), nullable=False)
            joined_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
            total_score = db.Column(db.Integer, default=0)
        
        class Problem(db.Model):
            __tablename__ = 'problems'
            id = db.Column(db.Integer, primary_key=True)
            title = db.Column(db.String(200), nullable=False)
            prompt_md = db.Column(db.Text, nullable=False)
            starter_code = db.Column(db.Text, nullable=False)
            tests_json = db.Column(db.Text, nullable=False)
            difficulty = db.Column(db.String(20), default='Easy')
        
        # Test database connection
        with app.app_context():
            db.create_all()
            print("✅ Database connected successfully!")
            database_connected = True
            
    except Exception as e:
        db_error_message = str(e)
        print(f"❌ Database connection failed: {e}")

# Routes
@app.route('/')
def index():
    if database_connected:
        try:
            problems = Problem.query.limit(10).all()
            return render_template_string("""
            <!DOCTYPE html>
            <html>
            <head>
                <title>StudySprint - Live!</title>
                <style>
                    body { font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; }
                    .success { color: green; font-weight: bold; font-size: 18px; }
                    .nav { background: #f8f9fa; padding: 10px; margin-bottom: 20px; border-radius: 5px; }
                    .nav a { margin-right: 15px; text-decoration: none; color: #007bff; }
                    .problem { border: 1px solid #ddd; padding: 15px; margin: 10px 0; border-radius: 5px; }
                </style>
            </head>
            <body>
                <div class="nav">
                    <a href="/">Home</a>
                    <a href="/problems">Problems</a>
                    <a href="/seed">Seed DB</a>
                </div>
                
                <h1>🚀 StudySprint is LIVE! ✅</h1>
                <p class="success">Your coding platform is working on Vercel with Supabase database!</p>
                
                <h2>🧠 Available Problems ({{ problems|length }})</h2>
                {% for problem in problems %}
                <div class="problem">
                    <h3>{{ problem.title }}</h3>
                    <p><strong>Difficulty:</strong> {{ problem.difficulty }}</p>
                    <p>{{ problem.prompt_md[:100] }}...</p>
                </div>
                {% endfor %}
                
                {% if problems|length == 0 %}
                <p>No problems yet. <a href="/seed">Click here to seed database with sample problems</a></p>
                {% endif %}
                
                <hr>
                <p><em>✅ Database: Connected | ✅ Flask: Running | ✅ Vercel: Deployed</em></p>
            </body>
            </html>
            """, problems=problems)
        except Exception as e:
            return f"<h1>Query Error</h1><p>{str(e)}</p>"
    else:
        # Database not connected - show fix instructions
        return render_template_string("""
        <!DOCTYPE html>
        <html>
        <head>
            <title>StudySprint - Database Issue</title>
            <style>
                body { font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; }
                .error { background: #fff3cd; border: 1px solid #ffeeba; padding: 15px; border-radius: 5px; margin: 15px 0; }
                .success { background: #d4edda; border: 1px solid #c3e6cb; padding: 15px; border-radius: 5px; margin: 15px 0; }
                .step { background: #f8f9fa; border-left: 4px solid #007bff; padding: 15px; margin: 10px 0; }
                code { background: #f8f9fa; padding: 2px 5px; border-radius: 3px; }
            </style>
        </head>
        <body>
            <h1>🔧 StudySprint Database Connection Issue</h1>
            
            <div class="success">
                <h3>✅ Good News!</h3>
                <p>Your Flask app is working perfectly on Vercel! Just need to fix the database connection.</p>
            </div>
            
            <div class="error">
                <h3>❌ Database Error:</h3>
                <p><code>{{ error_message }}</code></p>
            </div>
            
            <h2>🛠️ How to Fix:</h2>
            
            <div class="step">
                <h3>Step 1: Check Supabase Database</h3>
                <p>Go to <strong>supabase.com</strong> → Your Project</p>
                <p>If it says <strong>"Paused"</strong>, click <strong>"Resume"</strong></p>
            </div>
            
            <div class="step">
                <h3>Step 2: Verify Environment Variable</h3>
                <p>In Vercel Dashboard → Settings → Environment Variables</p>
                <p>Make sure <strong>DATABASE_URL</strong> is exactly:</p>
                <code>postgresql://postgres:studysprint123!@db.kfstzenkybnceicsjimu.supabase.co:5432/postgres</code>
                <p><em>(No brackets around the password!)</em></p>
            </div>
            
            <div class="step">
                <h3>Step 3: Redeploy</h3>
                <p>After fixing, click <strong>"Redeploy"</strong> in Vercel or wait for auto-deployment</p>
            </div>
            
            <hr>
            <p><a href="/health">Check Health Status</a> | <a href="/">Refresh Page</a></p>
        </body>
        </html>
        """, error_message=db_error_message or "Connection failed")

@app.route('/seed')
def seed():
    if not database_connected:
        return "<h1>❌ Database Not Connected</h1><p>Fix database connection first.</p><a href='/'>← Back</a>"
    
    try:
        if Problem.query.count() == 0:
            sample_problem = Problem(
                title="Two Sum",
                prompt_md="Given an array of integers, return indices of two numbers that add up to target.",
                starter_code="def solution(nums, target):\n    # Your code here\n    pass",
                tests_json='[{"input": [[2,7,11,15], 9], "output": [0,1]}]',
                difficulty="Easy"
            )
            db.session.add(sample_problem)
            db.session.commit()
            return "<h1>✅ Database Seeded!</h1><p>Sample problem added successfully!</p><a href='/'>← Go Home</a>"
        return "<h1>Already Seeded</h1><p>Database already has problems.</p><a href='/'>← Go Home</a>"
    except Exception as e:
        return f"<h1>Seed Error</h1><p>{str(e)}</p><a href='/'>← Back</a>"

@app.route('/problems')
def problems():
    if not database_connected:
        return "<h1>❌ Database Not Connected</h1><a href='/'>← Back</a>"
    try:
        problems = Problem.query.all()
        count = len(problems)
        return f"<h1>Problems ({count})</h1><p>Found {count} problems in database.</p><a href='/'>← Back</a>"
    except Exception as e:
        return f"<h1>Error</h1><p>{str(e)}</p><a href='/'>← Back</a>"

@app.route('/health')
def health():
    return {
        "status": "app_running",
        "database_url_set": bool(database_url),
        "database_connected": database_connected,
        "error": db_error_message,
        "app_type": "standalone_with_fallback"
    } 