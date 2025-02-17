import chromadb
import os
import logging
import shutil

logger = logging.getLogger(__name__)

class MemoryManager:
    def __init__(self):
        # Create a persistent directory for ChromaDB
        persist_dir = os.path.join(os.getcwd(), "chroma_storage")

        # Clean up existing storage to avoid conflicts
        if os.path.exists(persist_dir):
            try:
                shutil.rmtree(persist_dir)
                logger.info("Cleaned up existing ChromaDB storage")
            except Exception as e:
                logger.error(f"Error cleaning up ChromaDB storage: {str(e)}")

        # Create fresh directory
        os.makedirs(persist_dir, exist_ok=True)

        try:
            # Initialize ChromaDB client with persistent storage
            self.client = chromadb.PersistentClient(path=persist_dir)
            logger.info("ChromaDB client initialized with persistent storage")

            # Create collection
            self.collection = self.client.create_collection("conversations")
            logger.info("Created new conversations collection")

        except Exception as e:
            logger.error(f"Error initializing ChromaDB: {str(e)}")
            # Fallback to in-memory storage if persistent storage fails
            logger.info("Falling back to in-memory storage")
            self.client = chromadb.Client()
            self.collection = self.client.create_collection("conversations")

    def store_interaction(self, message, response):
        try:
            self.collection.add(
                documents=[f"{message}\n{response}"],
                metadatas=[{"type": "conversation"}],
                ids=[str(self.collection.count() + 1)]
            )
            logger.info("Stored new interaction successfully")
        except Exception as e:
            logger.error(f"Error storing interaction: {str(e)}")

    def get_context(self, query, n_results=5):
        try:
            if self.collection.count() == 0:
                logger.info("No previous conversations found")
                return ""

            results = self.collection.query(
                query_texts=[query],
                n_results=min(n_results, self.collection.count())
            )

            if results and results['documents']:
                return " ".join(results['documents'][0])
            return ""
        except Exception as e:
            logger.error(f"Error retrieving context: {str(e)}")
            return ""