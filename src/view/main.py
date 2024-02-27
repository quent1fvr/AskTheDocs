import streamlit as st
import os
import logging
import json
from src.view.usage_guide import streamlit_usage_guide
from src.view.log_view import StreamlitInterfaceLOG
from src.tools.folder_manager import FolderManager
dict_of_folders_path = os.getenv("DICT_OF_FOLDER_PATH")
from src.view.UI.ui_manager_admin import UIManagerAdmin
from src.view.UI.ui_manager_user import UIManagerUser  # Import UIManagerUser

class StreamlitApp:
    def __init__(self, chat, Dict_of_folders):
        self.chat = chat
        self.Dict_of_folders = Dict_of_folders
        self.ui_manager = UIManagerAdmin(Dict_of_folders, chat)  # UIManager instance
        self.ui_manager_user = UIManagerUser(chat)  # UIManagerUser instance
        
    def run(self):
        self.ui_manager_user.initialize_session_state()
        self.Dict_of_folders = FolderManager.load_folders(self.Dict_of_folders)

        view_type = self.setup_view_choice()

        if view_type == "User View":
            self.run_user_view()
        elif view_type == "Admin View":
            self.run_admin_view()
        # elif view_type == "Log View":
        #     self.interface_log.log_view()
        elif view_type == "Usage Guide":
            streamlit_usage_guide()

    def setup_view_choice(self):
        st.sidebar.title("Navigation")
        return st.sidebar.radio("Choose a View", ["User View", "Admin View"])

    def run_user_view(self):
        # Refactored to use UIManagerUser
        st.markdown("<h1 style='color: #ff9c3c; text-align: center; font-size: 60px;'> Ask SGFGAS  </h1>", unsafe_allow_html=True)
        query_type, Folders_list, selected_documents = self.ui_manager_user.setup_sidebar()  # Setup sidebar
        self.ui_manager_user.handle_user_query(query_type, selected_documents, Folders_list)


    def run_admin_view(self):
        st.markdown("<h1 style='color: #ff9c3c; text-align: center; font-size: 60px;'> Admin View </h1>", unsafe_allow_html=True)
        self.ui_manager.folder_creation_ui()  
        self.ui_manager.folder_management_ui()  
        self.ui_manager.document_deletion_ui()  
        self.ui_manager.folder_deletion_ui()  

# Main execution
if __name__ == "__main__":
    chat = None  # Initialize your Chatbot control here
    app = StreamlitApp(chat, dict_of_folders_path)  # Pass the folder path
    app.run()