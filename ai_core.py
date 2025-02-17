import logging
from utils.code_generator import CodeGenerator

logger = logging.getLogger(__name__)

class AICore:
    def __init__(self, memory_manager):
        self.memory_manager = memory_manager
        self.code_generator = CodeGenerator()
        logger.info("Initialized simplified AI Core")

    def process_message(self, message):
        try:
            # Store basic interaction
            response = self._generate_simple_response(message)
            self.memory_manager.store_interaction(message, response)
            return response
        except Exception as e:
            logger.error(f"Error processing message: {str(e)}")
            return "I'm sorry, I encountered an error. Please try again."

    def _generate_simple_response(self, message):
        # Simple template-based responses
        message = message.lower()
        if "hello" in message or "hi" in message:
            return "Hello! How can I help you today?"
        elif "code" in message or "generate" in message:
            return "I can help you generate code. Please specify what kind of code you need."
        elif "help" in message:
            return "I can help you with code generation and answer questions. What would you like to know?"
        else:
            return "I understand you want to discuss something. Could you please be more specific?"

    def generate_code(self, prompt):
        try:
            return self.code_generator.generate(prompt)
        except Exception as e:
            logger.error(f"Error generating code: {str(e)}")
            return "# Error generating code\nprint('Error: Please try again')"