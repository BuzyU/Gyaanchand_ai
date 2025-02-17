import chromadb
import os
import logging

logger = logging.getLogger(__name__)

class MemoryManager:
    def __init__(self):
        # Create a persistent directory for ChromaDB
        persist_dir = os.path.join(os.getcwd(), "chroma_storage")
        if not os.path.exists(persist_dir):
            os.makedirs(persist_dir)

        try:
            # Initialize ChromaDB client with the new configuration
            self.client = chromadb.PersistentClient(path=persist_dir)

            # Get or create the collection
            try:
                self.collection = self.client.get_collection("conversations")
            except ValueError:
                self.collection = self.client.create_collection("conversations")

        except Exception as e:
            logger.error(f"Error initializing ChromaDB: {str(e)}")
            # Fallback to in-memory storage if persistent storage fails
            self.client = chromadb.Client()
            self.collection = self.client.create_collection("conversations")

    def store_interaction(self, message, response):
        try:
            self.collection.add(
                documents=[f"{message}\n{response}"],
                metadatas=[{"type": "conversation"}],
                ids=[str(self.collection.count() + 1)]
            )
        except Exception as e:
            logger.error(f"Error storing interaction: {str(e)}")

    def get_context(self, query, n_results=5):
        try:
            results = self.collection.query(
                query_texts=[query],
                n_results=n_results
            )

            if results and results['documents']:
                return " ".join(results['documents'][0])
        except Exception as e:
            logger.error(f"Error retrieving context: {str(e)}")

        return ""