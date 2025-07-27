# Vercel entry point for StudySprint - Standalone Version
import os
from flask import Flask, render_template_string, request, redirect, session, jsonify, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import datetime

# Create Flask app
app = Flask(__name__)

# Database Configuration
database_url = os.environ.get('DATABASE_URL')
secret_key = os.environ.get('SECRET_KEY', 'fallback-secret-key')

if database_url:
    app.config["SQLALCHEMY_DATABASE_URI"] = database_url
    app.config["SECRET_KEY"] = secret_key
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    
    # Initialize database
    db = SQLAlchemy(app)
    
    # Define models directly here
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
        
        def get_tests(self):
            import json
            return json.loads(self.tests_json)
    
    # Initialize database tables
    with app.app_context():
        try:
            db.create_all()
            print("✅ Database initialized successfully")
        except Exception as e:
            print(f"❌ Database error: {e}")
    
    # Routes
    @app.route('/')
    def index():
        try:
            problems = Problem.query.limit(10).all()
            return render_template_string("""
            <!DOCTYPE html>
            <html>
            <head>
                <title>StudySprint - Live!</title>
                <style>
                    body { font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; }
                    .problem { border: 1px solid #ddd; padding: 15px; margin: 10px 0; border-radius: 5px; }
                    .success { color: green; font-weight: bold; }
                    .nav { background: #f8f9fa; padding: 10px; margin-bottom: 20px; border-radius: 5px; }
                    .nav a { margin-right: 15px; text-decoration: none; color: #007bff; }
                </style>
            </head>
            <body>
                <div class="nav">
                    <a href="/">Home</a>
                    <a href="/register">Register</a>
                    <a href="/login">Login</a>
                    <a href="/problems">Problems</a>
                </div>
                
                <h1>🚀 StudySprint is LIVE! ✅</h1>
                <p class="success">Your coding platform is working on Vercel!</p>
                
                <h2>🧠 Available Problems ({{ problems|length }})</h2>
                {% for problem in problems %}
                <div class="problem">
                    <h3>{{ problem.title }}</h3>
                    <p><strong>Difficulty:</strong> {{ problem.difficulty }}</p>
                    <p>{{ problem.prompt_md[:100] }}...</p>
                    <a href="/sprint/{{ problem.id }}">Start Sprint</a>
                </div>
                {% endfor %}
                
                {% if problems|length == 0 %}
                <p>No problems yet. <a href="/seed">Seed database with sample problems</a></p>
                {% endif %}
                
                <hr>
                <p><em>✅ Database: Connected | ✅ Flask: Running | ✅ Vercel: Deployed</em></p>
            </body>
            </html>
            """, problems=problems)
        except Exception as e:
            return f"<h1>Database Error</h1><p>{str(e)}</p>"
    
    @app.route('/problems')
    def problems():
        try:
            problems = Problem.query.all()
            return render_template_string("""
            <h1>All Problems</h1>
            {% for problem in problems %}
            <div style="border:1px solid #ccc; padding:10px; margin:10px;">
                <h3>{{ problem.title }}</h3>
                <p>Difficulty: {{ problem.difficulty }}</p>
            </div>
            {% endfor %}
            <a href="/">← Back to Home</a>
            """, problems=problems)
        except Exception as e:
            return f"Error: {str(e)}"
    
    @app.route('/seed')
    def seed():
        try:
            # Add a sample problem
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
                return "<h1>✅ Database Seeded!</h1><p>Sample problem added.</p><a href='/'>Go Home</a>"
            else:
                return "<h1>Already Seeded</h1><a href='/'>Go Home</a>"
        except Exception as e:
            return f"Seed Error: {str(e)}"

else:
    # No database URL
    @app.route('/')
    def config_error():
        return """
        <h1>🔧 Configuration Required</h1>
        <p>Set DATABASE_URL in Vercel environment variables.</p>
        """

@app.route('/health')
def health():
    return {
        "status": "ok",
        "database_url_set": bool(database_url),
        "app_type": "standalone_version"
    } 