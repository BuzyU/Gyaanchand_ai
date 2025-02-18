import os
import logging
from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from flask_cors import CORS

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)
# create the app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET")

# Enable CORS for all routes in production
CORS(app, resources={r"/api/*": {"origins": "*"}})

# configure the database to use SQLite with absolute path
db_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'gyaanchand.db')
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_path}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_recycle": 300,
    "pool_pre_ping": True,
}
# initialize the app with the extension
db.init_app(app)

with app.app_context():
    # Import models here
    import models  # noqa: F401
    try:
        logger.info("Creating database tables...")
        db.create_all()
        logger.info("Database tables created successfully")
    except Exception as e:
        logger.error(f"Error creating database tables: {str(e)}")
        # Don't raise the error if tables already exist
        if not "already exists" in str(e):
            raise

# Initialize AI components
from routes import init_routes
init_routes(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat')
def chat():
    return render_template('chat.html')

@app.route('/api/chat', methods=['POST'])
def handle_chat():
    try:
        data = request.json
        user_message = data.get('message', '')
        logger.debug(f"Received chat message: {user_message}")

        # Simple response generation (can be enhanced later)
        if "hello" in user_message.lower() or "hi" in user_message.lower():
            response = "Hello! How can I help you today?"
        elif "code" in user_message.lower():
            response = "I can help you generate code. What would you like to create?"
        else:
            response = "I understand you want to discuss something. Could you please be more specific?"

        return jsonify({
            'status': 'success',
            'response': response
        })
    except Exception as e:
        logger.error(f"Error in chat endpoint: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': 'An error occurred processing your request'
        }), 500

@app.route('/api/generate-code', methods=['POST'])
def generate_code():
    try:
        data = request.json
        prompt = data.get('prompt', '')
        logger.debug(f"Received code generation prompt: {prompt}")

        # Simple code generation (can be enhanced later)
        if "website" in prompt.lower():
            code = """
<!DOCTYPE html>
<html>
<head>
    <title>Generated Page</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body>
    <div class="container">
        <h1>Hello World</h1>
    </div>
</body>
</html>"""
        else:
            code = "print('Hello World')"

        return jsonify({
            'status': 'success',
            'code': code
        })
    except Exception as e:
        logger.error(f"Error in code generation endpoint: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': 'An error occurred generating code'
        }), 500