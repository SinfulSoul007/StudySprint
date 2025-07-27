# Some planning and boilerplate was generated or refined with the help of ChatGPT.
# I integrated and modified all code myself and take full responsibility.

from flask import Flask, render_template, request, redirect, session, jsonify, url_for, flash, abort
from models import db, User, Problem, Submission, Sprint
from werkzeug.security import generate_password_hash, check_password_hash
import datetime, json, subprocess, tempfile, os, uuid, sys
from sqlalchemy import func

app = Flask(__name__)

# Database Configuration - supports both local SQLite and cloud PostgreSQL
database_url = os.environ.get('DATABASE_URL')
if database_url:
    # Production: Use PostgreSQL from environment variable
    if database_url.startswith("postgres://"):
        database_url = database_url.replace("postgres://", "postgresql://", 1)
    app.config["SQLALCHEMY_DATABASE_URI"] = database_url
else:
    # Development: Use local SQLite
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///problems.db"

app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "dev-key-change-in-production")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

def run_test(code, test_input, expected_output):
    """
    Simple and naive test runner - runs user code with test input
    WARNING: This is not secure for production! Use Docker/sandboxing.
    """
    try:
        # Create a temporary file with the user's code
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            # Add the test input as variables at the top
            test_code = f"""
# Test input
test_input = {repr(test_input)}

# User's code
{code}

# Try to run the solution function
try:
    if 'solution' in locals():
        result = solution(test_input)
        print(result)
    else:
        print("Error: No 'solution' function found")
except Exception as e:
    print(f"Error: {{e}}")
"""
            f.write(test_code)
            temp_path = f.name
        
        # Run the code and capture output
        result = subprocess.run(
            [sys.executable, temp_path], 
            capture_output=True, 
            text=True, 
            timeout=5
        )
        
        # Clean up
        os.unlink(temp_path)
        
        if result.returncode == 0:
            output = result.stdout.strip()
            # Try to parse the output and compare with expected
            try:
                parsed_output = eval(output) if output else None
                return parsed_output == expected_output
            except:
                return output == str(expected_output)
        else:
            return False
            
    except Exception as e:
        return False

@app.route("/")
def index():
    """Home page showing available problems"""
    problems = Problem.query.limit(10).all()
    user_id = session.get('user_id')
    user = None
    if user_id:
        user = db.session.get(User, user_id)
    return render_template("index.html", problems=problems, user=user)

@app.route("/register", methods=["GET", "POST"])
def register():
    """User registration"""
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        
        # Check if user already exists
        if User.query.filter_by(username=username).first():
            flash("Username already exists!")
            return redirect(url_for('register'))
        
        # Create new user
        user = User(username=username, pass_hash=generate_password_hash(password))
        db.session.add(user)
        db.session.commit()
        
        # Log them in
        session['user_id'] = user.id
        session['username'] = user.username
        flash("Registration successful!")
        return redirect("/")
    
    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    """User login"""
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        
        user = User.query.filter_by(username=username).first()
        
        if user and check_password_hash(user.pass_hash, password):
            session['user_id'] = user.id
            session['username'] = user.username
            flash("Login successful!")
            return redirect("/")
        else:
            flash("Invalid username or password!")
    
    return render_template("login.html")

@app.route("/logout")
def logout():
    """User logout"""
    session.clear()
    flash("Logged out successfully!")
    return redirect("/")

@app.route("/sprint/<int:problem_id>")
def sprint(problem_id):
    """Start a 25-minute sprint for a problem"""
    if 'user_id' not in session:
        flash("Please login to start a sprint!")
        return redirect(url_for('login'))
    
    problem = db.session.get(Problem, problem_id) or abort(404)
    
    # Create a new sprint
    sprint = Sprint(user_id=session['user_id'], problem_id=problem_id)
    db.session.add(sprint)
    db.session.commit()
    
    session['current_sprint_id'] = sprint.id
    
    return render_template("sprint.html", problem=problem, sprint=sprint)

@app.route("/submit/<int:problem_id>", methods=["POST"])
def submit(problem_id):
    """Submit code for a problem and run tests"""
    if 'user_id' not in session:
        return jsonify({"error": "Not logged in"}), 401
    
    code = request.json.get("code", "")
    solve_time = request.json.get("solve_time", 0)  # Time in seconds from frontend
    problem = db.session.get(Problem, problem_id) or abort(404)
    
    # Create submission record
    submission = Submission(
        user_id=session['user_id'], 
        problem_id=problem_id, 
        code=code,
        solve_time_seconds=solve_time
    )
    db.session.add(submission)
    db.session.commit()
    
    # Run tests
    tests = problem.get_tests()
    passed_count = 0
    total_tests = len(tests)
    test_results = []
    
    for i, test in enumerate(tests):
        passed = run_test(code, test["input"], test["output"])
        if passed:
            passed_count += 1
        test_results.append({
            "test_number": i + 1,
            "passed": passed,
            "input": test["input"],
            "expected": test["output"]
        })
    
    # Update submission
    all_passed = passed_count == total_tests
    submission.passed = all_passed
    
    # Calculate and award points if passed
    points_earned = 0
    if all_passed:
        points_earned = submission.calculate_points()
        submission.points_earned = points_earned
        
        # Update user's total score
        user = db.session.get(User, session['user_id'])
        user.total_score += points_earned
    
    db.session.commit()
    
    # Update sprint if completed
    sprint_id = session.get('current_sprint_id')
    if sprint_id:
        sprint = db.session.get(Sprint, sprint_id)
        if sprint and not sprint.completed:
            sprint.finished_at = datetime.datetime.utcnow()
            sprint.completed = all_passed
            sprint.solve_time_seconds = solve_time
            db.session.commit()
    
    return jsonify({
        "passed": all_passed,
        "tests_passed": passed_count,
        "total_tests": total_tests,
        "results": test_results,
        "points_earned": points_earned,
        "solve_time": f"{solve_time // 60:02d}:{solve_time % 60:02d}" if solve_time else "N/A"
    })

@app.route("/dashboard")
def dashboard():
    """User dashboard showing stats and progress"""
    if 'user_id' not in session:
        flash("Please login to view dashboard!")
        return redirect(url_for('login'))
    
    user = db.session.get(User, session['user_id'])
    
    # Get submission stats
    total_submissions = Submission.query.filter_by(user_id=user.id).count()
    passed_submissions = Submission.query.filter_by(user_id=user.id, passed=True).count()
    failed_submissions = total_submissions - passed_submissions
    
    # Get recent submissions
    recent_submissions = Submission.query.filter_by(user_id=user.id)\
        .order_by(Submission.submitted_at.desc())\
        .limit(10).all()
    
    # Get problem difficulty breakdown
    difficulty_stats = db.session.query(
        Problem.difficulty, 
        func.count(Submission.id).label('count')
    ).join(Submission).filter(
        Submission.user_id == user.id, 
        Submission.passed == True
    ).group_by(Problem.difficulty).all()
    
    return render_template("dashboard.html", 
                         user=user,
                         total_submissions=total_submissions,
                         passed_submissions=passed_submissions,
                         failed_submissions=failed_submissions,
                         recent_submissions=recent_submissions,
                         difficulty_stats=difficulty_stats)

@app.route("/problems")
def problems():
    """Browse all problems with filtering"""
    difficulty = request.args.get('difficulty', '')
    tag = request.args.get('tag', '')
    
    query = Problem.query
    
    if difficulty:
        query = query.filter(Problem.difficulty == difficulty)
    
    if tag:
        query = query.filter(Problem.tags.contains(tag))
    
    problems = query.all()
    
    # Get all unique difficulties and tags for filtering
    difficulties = db.session.query(Problem.difficulty).distinct().all()
    all_tags = set()
    for problem in Problem.query.all():
        all_tags.update(problem.get_tags_list())
    
    return render_template("problems.html", 
                         problems=problems,
                         difficulties=[d[0] for d in difficulties],
                         tags=sorted(all_tags),
                         current_difficulty=difficulty,
                         current_tag=tag)

@app.route("/leaderboard")
def leaderboard():
    """Global leaderboard showing top performers"""
    # Get top users by total score
    top_users = User.query.filter(User.total_score > 0)\
        .order_by(User.total_score.desc())\
        .limit(20).all()
    
    # Get fastest solves for each problem
    fastest_solves = []
    problems = Problem.query.all()
    for problem in problems:
        fastest = problem.get_fastest_solve()
        if fastest:
            fastest_solves.append({
                'problem': problem,
                'time': fastest.solve_time_seconds,
                'username': fastest.username,
                'formatted_time': f"{fastest.solve_time_seconds // 60:02d}:{fastest.solve_time_seconds % 60:02d}"
            })
    
    return render_template("leaderboard.html", 
                         top_users=top_users,
                         fastest_solves=fastest_solves)

@app.route("/problem/<int:problem_id>/leaderboard")
def problem_leaderboard(problem_id):
    """Leaderboard for a specific problem"""
    problem = db.session.get(Problem, problem_id) or abort(404)
    leaderboard_data = problem.get_leaderboard(limit=20)
    
    # Format the data for display
    formatted_data = []
    for rank, (username, solve_time, submitted_at) in enumerate(leaderboard_data, 1):
        formatted_data.append({
            'rank': rank,
            'username': username,
            'solve_time': solve_time,
            'formatted_time': f"{solve_time // 60:02d}:{solve_time % 60:02d}",
            'submitted_at': submitted_at
        })
    
    return render_template("problem_leaderboard.html", 
                         problem=problem,
                         leaderboard=formatted_data)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=3000) 