import logging
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
    """Initialize AI components"""
    logger.info("Starting route initialization...")

    if not init_ai_components():
        logger.error("Failed to initialize AI components. Routes will be available but AI features may not work.")

    logger.info("Route initialization completed")