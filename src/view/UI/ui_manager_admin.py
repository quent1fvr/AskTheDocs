import streamlit as st
from src.tools.folder_manager import FolderManager
import logging
import time
import tempfile

class UIManagerAdmin:
    def __init__(self, Dict_of_folders, ctrl):
        self.Dict_of_folders = FolderManager.load_folders(Dict_of_folders)
        self.ctrl = ctrl

    def folder_creation_ui(self):
        with st.expander("Document Management", expanded=True):
            actual_page_start = st.number_input("Start page (default = 1)", value=1, min_value=1, key="actual_page_start")
            include_images = st.checkbox("Analyze text from images (ONLY for .pdf)", value=False, key="include_images")
            uploaded_file = st.file_uploader("Upload a file", key="input_doc_comp")

            if st.button("Process File", key="process_file_button"):
                if uploaded_file is not None:
                    original_file_name = uploaded_file.name
                    with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
                        tmp_file.write(uploaded_file.getvalue())
                        tmp_file_path = tmp_file.name

                    start_time = time.time()
                    result = self.ctrl.upload_doc(tmp_file_path, include_images, actual_page_start, original_file_name)
                    end_time = time.time()

                    if result:
                        st.success('File processed successfully.')
                        folder_names = FolderManager.get_folder_names(self.Dict_of_folders)
                        if 'Default' in folder_names:
                            default_folder_index = folder_names.index('Default')
                            self.Dict_of_folders["entries"][default_folder_index]["files"].append(original_file_name)
                            FolderManager.save_folders(self.Dict_of_folders)
                        else:
                            st.error("Default folder not found.")

                        logging.info(f"Execution time for upload_doc: {end_time - start_time} seconds")
                    else:
                        st.error("File extension not supported. Only .docx, .pdf, and .html are supported.")

            if st.button("Clear File", key="clear_file_button"):
                st.session_state['input_doc_comp'] = None


    def folder_management_ui(self):
        with st.expander("Collection management", expanded=False):
            self._create_new_folder_ui()
            st.subheader("Manage Existing Collections")
            folder_names = FolderManager.get_folder_names(self.Dict_of_folders)
            if not folder_names:
                st.write("No folders to display.")
                return

            selected_folder_name = st.selectbox("Select a collection to manage", folder_names, key="selected_folder_to_manage")
            selected_folder = FolderManager.find_folder(self.Dict_of_folders, selected_folder_name)
            if selected_folder:
                UIManagerAdmin.display_current_files(selected_folder["files"])
                self._manage_existing_folder(selected_folder, selected_folder_name)

    @staticmethod
    def confluence_management_ui():
        with st.expander("Confluence Management", expanded=False):
            st.subheader("Confluence Management")
            st.write("This feature is not yet implemented.")
            st.write("Please check back later.")

    @staticmethod
    def display_current_files(files):
        if files:
            file_list = '\n'.join(f"- {file}" for file in files)
            st.markdown("### Current files in the collection:\n" + file_list)
        else:
            st.write("No files in the folder.")

    def submit_manual_feedback(self, feedback_text):
        """Submits manual feedback."""
        if feedback_text:
            self.handle_feedback("Manual", feedback_text)
            
    def document_deletion_ui(self):
        with st.expander("Document deletion", expanded=False):
            all_documents = UIManagerAdmin.get_all_documents(self.ctrl)
            selected_file_to_delete = st.selectbox("Select a file to delete", options=set(all_documents), key="select_file_to_delete")

            if st.button("Delete File", key="delete_file_button"):
                if selected_file_to_delete:
                    self.delete_file(selected_file_to_delete)
                    

    def folder_deletion_ui(self):
        with st.expander("Collection deletion", expanded=False):
            all_folders = [folder['name'] for folder in self.Dict_of_folders['entries']]
            selected_folder_to_delete = st.selectbox("Select a folder to delete", options=all_folders, key="select_folder_to_delete")

            if st.button("Delete Folder", key="delete_folder_button"):
                if selected_folder_to_delete:
                    self.delete_folder(selected_folder_to_delete)

    @staticmethod
    def get_all_documents(ctrl):
        try:
            all_documents = ctrl.retriever.collection.get()['metadatas']
            return [doc['doc'] for doc in all_documents]
        except Exception as e:
            logging.error("Failed to retrieve document IDs: " + str(e))
            return []

    def delete_file(self, file_name):
        try:
            self.ctrl.retriever.collection.delete(where={"doc": file_name})
            for folder in self.Dict_of_folders["entries"]:
                if file_name in folder["files"]:
                    folder["files"].remove(file_name)
            FolderManager.save_folders(self.Dict_of_folders)
            st.success(f"File '{file_name}' deleted successfully.")
        except Exception as e:
            st.error(f"Error in deleting file '{file_name}': {e}")
            
    def delete_folder(self, folder_name):
        try:
            if folder_name not in [folder['name'] for folder in self.Dict_of_folders['entries']]:
                st.error(f"Folder '{folder_name}' does not exist.")
                return

            self.Dict_of_folders["entries"] = [folder for folder in self.Dict_of_folders["entries"] if folder["name"] != folder_name]
            FolderManager.save_folders(self.Dict_of_folders)
            st.success(f"Collection '{folder_name}' and its files deleted successfully.")
        except Exception as e:
            st.error(f"Error in deleting collection '{folder_name}': {e}")

    def _create_new_folder_ui(self):
        st.subheader("Create New Collection")
        new_folder_name = st.text_input("Collection Name", key="new_folder_name")
        try:
            all_documents = [item['doc'] for item in self.ctrl.retriever.collection.get()['metadatas']]
        except Exception as e:
            st.error("Failed to retrieve documents: " + str(e))
            return

        selected_documents = st.multiselect("Select documents to add", set(all_documents), key="selected_documents_for_new_folder")
        if st.button("Create Collection", key="create_folder_button"):
            if not new_folder_name:
                st.warning("Please enter a name for the folder.")
                return
            existing_folder = FolderManager.find_folder(self.Dict_of_folders, new_folder_name)
            if existing_folder and not st.checkbox(f"A folder named '{new_folder_name}' already exists. Do you want to overwrite it?"):
                return
            FolderManager.create_folder(new_folder_name, selected_documents, self.Dict_of_folders)
            st.success(f"Collection '{new_folder_name}' created successfully.")

    def _manage_existing_folder(self, selected_folder, selected_folder_name):
        try:
            all_documents = [item['doc'] for item in self.ctrl.retriever.collection.get()['metadatas']]
        except Exception as e:
            st.error("Failed to retrieve documents: " + str(e))
            return

        additional_documents = st.multiselect("Add more documents to the collection", 
                                              set([doc for doc in all_documents if doc not in selected_folder["files"]]), 
                                              key="additional_documents")
        files_to_remove = st.multiselect("Select files to remove from the collection", 
                                        selected_folder["files"], 
                                        key="files_to_remove")
        if st.button("Update Collection", key="update_folder_button"):
            updated_files = [doc for doc in selected_folder["files"] if doc not in files_to_remove] + additional_documents
            FolderManager.create_folder(selected_folder_name, updated_files, self.Dict_of_folders)
            st.success(f"Collection '{selected_folder_name}' updated.")
            st.experimental_rerun()
        if st.button("Remove Collection", key="remove_folder_button"):
            if st.checkbox(f"Are you sure you want to remove the collection '{selected_folder_name}'?"):
                FolderManager.remove_folder(selected_folder_name, self.Dict_of_folders)
                st.success(f"Collection '{selected_folder_name}' and its files removed.")
                st.experimental_rerun()


