from mistralai.client import MistralClient
from src.Llm.llm import LlmAgent
from src.view.main import StreamlitApp
from config import Config
from initializer import Initializer

def main():
    """Main function to run the Streamlit app."""
    config = Config()
    initializer = Initializer(config)

    initializer.initialize_logging()

    mistral_client = MistralClient(config.mistral_api_key)
    llm_agent = LlmAgent(config.llm_model, mistral_client)

    client_db, collection = initializer.initialize_database()
    chat = initializer.initialize_chatbot(client_db, llm_agent,collection)

    app = StreamlitApp(chat, config.dict_of_folders)
    app.run()

if __name__ == "__main__":
    main()
