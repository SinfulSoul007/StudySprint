# Some planning and database schema was generated or refined with the help of ChatGPT.
# I integrated and modified all code myself and take full responsibility.

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    pass_hash = db.Column(db.String(255), nullable=False)
    joined_at = db.Column(db.DateTime, default=datetime.utcnow)
    streak_count = db.Column(db.Integer, default=0)
    total_score = db.Column(db.Integer, default=0)  # New: Total points earned
    
    # Relationships
    submissions = db.relationship('Submission', backref='user', lazy=True)
    sprints = db.relationship('Sprint', backref='user', lazy=True)
    
    def calculate_rank(self):
        """Calculate user's global rank based on total score"""
        higher_scores = User.query.filter(User.total_score > self.total_score).count()
        return higher_scores + 1
    
    def get_fastest_solves(self):
        """Get user's fastest solve times"""
        return db.session.query(Submission.problem_id, db.func.min(Submission.solve_time_seconds))\
            .filter(Submission.user_id == self.id, Submission.passed == True)\
            .group_by(Submission.problem_id).all()
    
    def __repr__(self):
        return f'<User {self.username}>'

class Problem(db.Model):
    __tablename__ = 'problems'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    prompt_md = db.Column(db.Text, nullable=False)
    starter_code = db.Column(db.Text, nullable=False)
    tests_json = db.Column(db.Text, nullable=False)  # JSON string of test cases
    tags = db.Column(db.String(500))  # Comma-separated tags
    difficulty = db.Column(db.String(20), default='Easy')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    points = db.Column(db.Integer, default=100)  # New: Points awarded for solving
    
    # Relationships
    submissions = db.relationship('Submission', backref='problem', lazy=True)
    
    def get_tests(self):
        """Parse and return test cases as Python objects"""
        return json.loads(self.tests_json)
    
    def get_tags_list(self):
        """Return tags as a list"""
        return [tag.strip() for tag in self.tags.split(',') if tag.strip()]
    
    def get_fastest_solve(self):
        """Get the fastest solve time for this problem"""
        fastest = db.session.query(
            Submission.solve_time_seconds,
            User.username
        ).join(User).filter(
            Submission.problem_id == self.id,
            Submission.passed == True,
            Submission.solve_time_seconds.isnot(None)
        ).order_by(Submission.solve_time_seconds.asc()).first()
        
        return fastest
    
    def get_leaderboard(self, limit=10):
        """Get leaderboard for this problem"""
        return db.session.query(
            User.username,
            Submission.solve_time_seconds,
            Submission.submitted_at
        ).join(Submission).filter(
            Submission.problem_id == self.id,
            Submission.passed == True,
            Submission.solve_time_seconds.isnot(None)
        ).order_by(Submission.solve_time_seconds.asc()).limit(limit).all()
    
    def __repr__(self):
        return f'<Problem {self.title}>'

class Submission(db.Model):
    __tablename__ = 'submissions'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    problem_id = db.Column(db.Integer, db.ForeignKey('problems.id'), nullable=False)
    code = db.Column(db.Text, nullable=False)
    passed = db.Column(db.Boolean, default=False)
    runtime_ms = db.Column(db.Integer)
    solve_time_seconds = db.Column(db.Integer)  # New: Time taken to solve (in seconds)
    submitted_at = db.Column(db.DateTime, default=datetime.utcnow)
    points_earned = db.Column(db.Integer, default=0)  # New: Points earned for this submission
    
    def calculate_points(self):
        """Calculate points based on difficulty and solve time"""
        if not self.passed:
            return 0
        
        base_points = self.problem.points
        
        # Bonus points for speed (if solved in under certain time)
        speed_bonus = 0
        if self.solve_time_seconds:
            if self.solve_time_seconds < 60:  # Under 1 minute
                speed_bonus = 50
            elif self.solve_time_seconds < 300:  # Under 5 minutes
                speed_bonus = 25
            elif self.solve_time_seconds < 900:  # Under 15 minutes
                speed_bonus = 10
        
        # Difficulty multiplier
        difficulty_multiplier = {
            'Easy': 1.0,
            'Medium': 1.5,
            'Hard': 2.0
        }.get(self.problem.difficulty, 1.0)
        
        total_points = int((base_points + speed_bonus) * difficulty_multiplier)
        return total_points
    
    def format_solve_time(self):
        """Format solve time as MM:SS"""
        if not self.solve_time_seconds:
            return "N/A"
        
        minutes = self.solve_time_seconds // 60
        seconds = self.solve_time_seconds % 60
        return f"{minutes:02d}:{seconds:02d}"
    
    def __repr__(self):
        return f'<Submission {self.id} - {"Passed" if self.passed else "Failed"}>'

class Sprint(db.Model):
    __tablename__ = 'sprints'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    problem_id = db.Column(db.Integer, db.ForeignKey('problems.id'), nullable=True)
    started_at = db.Column(db.DateTime, default=datetime.utcnow)
    finished_at = db.Column(db.DateTime)
    completed = db.Column(db.Boolean, default=False)
    solve_time_seconds = db.Column(db.Integer)  # New: Actual time taken to solve
    
    def get_duration_seconds(self):
        """Calculate sprint duration in seconds"""
        if not self.finished_at:
            return None
        return int((self.finished_at - self.started_at).total_seconds())
    
    def __repr__(self):
        return f'<Sprint {self.id} - {"Completed" if self.completed else "In Progress"}>' 