import os
import logging.config
import chromadb
from src.control.control import Chatbot
from src.tools.retriever import Retriever

class Initializer:
    def __init__(self, config):
        self.config = config

    def initialize_logging(self):
        """Initializes logging configuration."""
        logging.config.fileConfig(self.config.logging_config_file_path)

    def initialize_database(self):
        """Initializes and returns the database and collection."""
        if not os.path.exists(self.config.database_path): 
            os.makedirs(self.config.database_path)
        client_db = chromadb.PersistentClient(self.config.database_path)
        collection = client_db.get_or_create_collection(self.config.collection_name)
        return client_db, collection

    def initialize_chatbot(self, client_db, llm_agent, collection):
        """Initializes and returns the chatbot instance."""
        return Chatbot(client_db=client_db, llm_agent=llm_agent, retriever=Retriever(llmagent=llm_agent, collection=collection))
