# Vercel entry point for StudySprint
import sys
import os

# Add parent directory to path so we can import from root
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    # Import the full StudySprint app
    from app import app
    print("✅ StudySprint app imported successfully")
    
except Exception as import_error:
    print(f"❌ Import error: {import_error}")
    # Fallback to minimal Flask app
    from flask import Flask
    app = Flask(__name__)
    
    @app.route('/')
    def error_page():
        return f"""
        <h1>🚨 StudySprint Import Error</h1>
        <p><strong>Error:</strong> {import_error}</p>
        <p>Check Vercel function logs for details.</p>
        <a href="/health">Health Check</a>
        """
    
    @app.route('/health')
    def health():
        return {"status": "error", "message": str(import_error)}

# Test route to verify the app is working
@app.route('/test')
def test():
    return """
    <h1>🚀 StudySprint Test Page</h1>
    <p>✅ Vercel serverless function is working!</p>
    <p>🐍 Python Flask is running correctly</p>
    <p>🔧 Full app should be loaded now!</p>
    <a href="/">Go to StudySprint Home</a>
    """ 