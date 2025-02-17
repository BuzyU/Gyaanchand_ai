import os
import logging
import sqlite3
from datetime import datetime

logger = logging.getLogger(__name__)

class MemoryManager:
    def __init__(self):
        self.db_path = os.path.join(os.getcwd(), "memory.db")
        self._init_db()

    def _init_db(self):
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                # Create table for storing conversations
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS conversations (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        message TEXT NOT NULL,
                        response TEXT NOT NULL,
                        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                    )
                """)
                conn.commit()
                logger.info("Memory database initialized successfully")
        except Exception as e:
            logger.error(f"Error initializing memory database: {str(e)}")

    def store_interaction(self, message, response):
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO conversations (message, response) VALUES (?, ?)",
                    (message, response)
                )
                conn.commit()
                logger.info("Stored new interaction successfully")
        except Exception as e:
            logger.error(f"Error storing interaction: {str(e)}")

    def get_context(self, query, n_results=5):
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                # Get the most recent conversations as context
                cursor.execute(
                    "SELECT message, response FROM conversations ORDER BY timestamp DESC LIMIT ?",
                    (n_results,)
                )
                results = cursor.fetchall()
                if not results:
                    logger.info("No previous conversations found")
                    return ""

                # Combine messages and responses into context
                context = " ".join([f"{msg}\n{resp}" for msg, resp in results])
                return context
        except Exception as e:
            logger.error(f"Error retrieving context: {str(e)}")
            return ""