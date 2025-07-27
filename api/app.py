# Vercel entry point for StudySprint - Progressive Loading
from flask import Flask

# Create basic Flask app first
app = Flask(__name__)

@app.route('/')
def home():
    return """
    <h1>🔧 StudySprint Debug Mode</h1>
    <p>Testing imports step by step...</p>
    <ul>
        <li><a href="/test1">Test 1: Basic Flask ✅</a></li>
        <li><a href="/test2">Test 2: Import os/sys</a></li>
        <li><a href="/test3">Test 3: Path manipulation</a></li>
        <li><a href="/test4">Test 4: Import models</a></li>
        <li><a href="/test5">Test 5: Import main app</a></li>
    </ul>
    """

@app.route('/test1')
def test1():
    return {"status": "✅ Basic Flask working", "test": "test1"}

@app.route('/test2')
def test2():
    try:
        import os
        import sys
        return {"status": "✅ os/sys imported", "python_version": sys.version}
    except Exception as e:
        return {"status": "❌ Import failed", "error": str(e)}

@app.route('/test3')
def test3():
    try:
        import os
        import sys
        current_dir = os.path.dirname(os.path.abspath(__file__))
        parent_dir = os.path.dirname(current_dir)
        sys.path.insert(0, parent_dir)
        return {"status": "✅ Path manipulation working", "parent_dir": parent_dir}
    except Exception as e:
        return {"status": "❌ Path manipulation failed", "error": str(e)}

@app.route('/test4')
def test4():
    try:
        import os
        import sys
        sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        from models import db, User, Problem
        return {"status": "✅ Models imported successfully"}
    except Exception as e:
        return {"status": "❌ Models import failed", "error": str(e)}

@app.route('/test5')
def test5():
    try:
        import os
        import sys
        sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        from app import app as main_app
        return {"status": "✅ Main app imported successfully"}
    except Exception as e:
        return {"status": "❌ Main app import failed", "error": str(e)} 