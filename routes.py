import logging
from flask import render_template, request, jsonify
from utils.memory_manager import MemoryManager
from ai_core import AICore

logger = logging.getLogger(__name__)

# Global variables to store AI components
memory_manager = None
ai_core = None

def init_ai_components():
    """Initialize AI components with proper error handling"""
    global memory_manager, ai_core

    try:
        logger.info("Initializing Memory Manager...")
        memory_manager = MemoryManager()
        logger.info("Memory Manager initialized successfully")

        logger.info("Initializing AI Core...")
        ai_core = AICore(memory_manager)
        logger.info("AI Core initialized successfully")

        return True
    except Exception as e:
        logger.error(f"Failed to initialize AI components: {str(e)}")
        return False

def init_routes(app):
    """Initialize routes and AI components"""
    logger.info("Starting route initialization...")

    if not init_ai_components():
        logger.error("Failed to initialize AI components. Routes will be available but AI features may not work.")

    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/chat')
    def chat():
        return render_template('chat.html')

    @app.route('/api/chat', methods=['POST'])
    def process_chat():
        if not ai_core:
            return jsonify({
                'status': 'error',
                'message': 'AI system is not initialized'
            }), 503

        try:
            data = request.json
            user_message = data.get('message', '')
            logger.debug(f"Processing chat message: {user_message}")

            response = ai_core.process_message(user_message)

            return jsonify({
                'status': 'success',
                'response': response
            })
        except Exception as e:
            logger.error(f"Error processing chat: {str(e)}")
            return jsonify({
                'status': 'error',
                'message': 'An error occurred processing your request'
            }), 500

    @app.route('/api/generate-code', methods=['POST'])
    def generate_code():
        if not ai_core:
            return jsonify({
                'status': 'error',
                'message': 'AI system is not initialized'
            }), 503

        try:
            data = request.json
            prompt = data.get('prompt', '')
            logger.debug(f"Generating code for prompt: {prompt}")

            code = ai_core.generate_code(prompt)

            return jsonify({
                'status': 'success',
                'code': code
            })
        except Exception as e:
            logger.error(f"Error generating code: {str(e)}")
            return jsonify({
                'status': 'error',
                'message': 'An error occurred generating code'
            }), 500

    logger.info("Route initialization completed")