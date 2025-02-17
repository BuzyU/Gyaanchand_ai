from datetime import datetime
from app import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    chats = db.relationship('Chat', backref='user', lazy='dynamic')
    code_generations = db.relationship('CodeGeneration', backref='user', lazy='dynamic')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Chat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    message = db.Column(db.Text, nullable=False)
    response = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    context_id = db.Column(db.String(64))  # For tracking conversation context
    
    def to_dict(self):
        return {
            'id': self.id,
            'message': self.message,
            'response': self.response,
            'created_at': self.created_at.isoformat(),
            'context_id': self.context_id
        }

class CodeGeneration(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    prompt = db.Column(db.Text, nullable=False)
    generated_code = db.Column(db.Text, nullable=False)
    language = db.Column(db.String(32))  # e.g., 'python', 'html', 'javascript'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'prompt': self.prompt,
            'generated_code': self.generated_code,
            'language': self.language,
            'created_at': self.created_at.isoformat()
        }

class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    content_type = db.Column(db.String(32))  # 'chat' or 'code'
    content_id = db.Column(db.Integer, nullable=False)  # ID of Chat or CodeGeneration
    rating = db.Column(db.Integer)  # 1-5 rating
    comment = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
