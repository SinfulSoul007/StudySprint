# Vercel entry point for StudySprint - MINIMAL TEST VERSION
from flask import Flask

# Create minimal Flask app for testing
app = Flask(__name__)

@app.route('/')
def test():
    return """
    <h1>🚀 StudySprint Test Page</h1>
    <p>✅ Vercel serverless function is working!</p>
    <p>🐍 Python Flask is running correctly</p>
    <p>🔧 Next: Add database connection</p>
    """

@app.route('/health')
def health():
    return {"status": "ok", "message": "Serverless function is working"}

# For development testing
if __name__ == "__main__":
    app.run() 