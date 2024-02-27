from dotenv import load_dotenv
import os
class Config:
    """Handles the configuration settings for the application with validation."""

    def __init__(self):
        load_dotenv()
        self.llm_model = self.get_env_variable("LLM_MODEL")    
        self.logging_config_file_path = self.get_env_variable("LOGGING_CONFIG_FILE_PATH")
        self.dict_of_folders = self.get_env_variable("FOLDERS_PATH")
        self.mistral_api_key = self.get_env_variable("MISTRAL_API_KEY")
        self.collection_name = self.get_env_variable("COLLECTION_NAME")
        self.database_path = self.get_env_variable("DATABASE_PATH")

    @staticmethod
    def get_env_variable(var_name):
        """Retrieves and validates an environment variable."""
        value = os.getenv(var_name)
        if value is None:
            raise ValueError(f"Environment variable {var_name} not set.")
        return value
