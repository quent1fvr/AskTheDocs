import streamlit as st
import logging
from src.tools.folder_manager import FolderManager
import os
class UIManagerUser:
    def __init__(self, ctrl):
        self.ctrl = ctrl
        self.initialize_session_state()
        
        
    def setup_sidebar(self):
        Dict_of_folders = os.getenv("FOLDERS_PATH")
        Dict_of_folders = FolderManager.load_folders(Dict_of_folders)
        st.sidebar.title("Document Selection")
        query_type = st.sidebar.radio("", options=["Everything", "Collection", "Document(s)"])
        Folders_list, selected_documents = [], []
        if query_type == "Collection":
            Folders_list = st.sidebar.multiselect("Select Collection", options=FolderManager.get_folder_names(Dict_of_folders), key="Folders_list")
        elif query_type == "Document(s)":
            all_documents = set(doc for folder in Dict_of_folders["entries"] for doc in folder["files"])
            selected_documents = st.sidebar.multiselect("Select Document(s)", options=all_documents, key="Documents_in_folder")
        st.sidebar.title("Feedbacks")
        col1, col2 = st.sidebar.columns(2)
        with col1:
            if col1.button("👍 Positive"):
                self.handle_feedback("Positive")

        with col2:
            if col2.button("👎 Negative"):
                self.handle_feedback("Negative")
        st.sidebar.title("Manual Feedback")
        feedback_text = st.sidebar.text_input("Enter your feedback", key="manual_feedback")
        
        if st.sidebar.button("Submit Manual Feedback", on_click=self._on_feedback_submit(feedback_text)):
            pass
        
        st.sidebar.button('Reset Chat',on_click=self.reset_conversation)
    
        st.sidebar.title("Example Queries")
        st.session_state['selected_example_query'] = st.sidebar.selectbox("Choose an example query", st.session_state['example_queries'])
        self.display_chat()

        if st.sidebar.button("Use Selected Query"):
            self.handle_user_query_with_example(st.session_state['selected_example_query'],query_type, selected_documents, Folders_list)
            
        return query_type, Folders_list, selected_documents
        
    def handle_user_query_with_example(self, user_query,query_type,selected_documents,folders_list):
            with st.spinner('Please wait...'):
                self.add_message_to_chat({"role": "user", "content": user_query})
                response, sources = self.get_response(user_query, query_type, selected_documents, folders_list)
                self.add_message_to_chat({"role": "bot", "content": response})
                self.display_chat()
                self.update_sources_info(sources, query_type)
    
    
    def handle_feedback(self, feedback_type, feedback_content=""):
        """Logs feedback received from users."""
        if feedback_type == "Manual":
            logging.info(f"Feedback: {feedback_content} ", extra={'category': 'Manual Feedback', 'elapsed_time': 0})
        else:
            query, answer, sources_contents = self._extract_feedback_details()
            logging.info(f"Feedback: {feedback_type}, Collection: Eureka, Query: {query}, Answer: {answer}, Sources: {sources_contents}", extra={'category': 'Thumb Feedback', 'elapsed_time': 0})

    def handle_user_query(self, query_type, selected_documents, folders_list):
        user_query = st.chat_input("Ask your question here")
        if user_query:
            with st.spinner('Please wait...'):
                self.add_message_to_chat({"role": "user", "content": user_query})
                response, sources = self.get_response(user_query, query_type, selected_documents, folders_list)
                self.add_message_to_chat({"role": "bot", "content": response})
                self.display_chat()
                self.update_sources_info(sources, query_type)

    def get_response(self, user_query, query_type, selected_documents, folders_list):
        if query_type == "Model only":
            response = self.ctrl.get_response_llm(query=user_query, histo=st.session_state['messages'])
            sources = []
        else:
            documents = selected_documents if query_type in ["Folder", "Document(s)"] else []
            response, sources = self.ctrl.get_response(query=user_query, histo=st.session_state['messages'], folder=folders_list, doc_or_folder=query_type, documents=documents)
        return response, sources

    def display_chat(self):
        for message in st.session_state['messages']:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

    def update_sources_info(self, sources, query_type):
        if query_type != "No Documents" and sources:
            st.session_state['sources_info'] = [(source.index, source.title, source.distance_str, source.content) for source in sources[:3]]
            self.display_sources()

    def display_sources(self):
        if st.session_state['sources_info']:
            with st.expander("View Sources"):
                for index, (source_index, title, score, content) in enumerate(st.session_state['sources_info']):
                    st.markdown(f"**Source {source_index}: {title}** (score = {score})")
                    st.text_area(f"source_content_{index}", value=content, height=100, disabled=True, key=f"source_content_{index}")


    def initialize_session_state(self):
        if 'clear_chat_flag' not in st.session_state:
            st.session_state['clear_chat_flag'] = False
        if 'messages' not in st.session_state:
            st.session_state['messages'] = []
        if 'sources_info' not in st.session_state:
            st.session_state['sources_info'] = []
        if 'example_queries' not in st.session_state:
            st.session_state['example_queries'] = ["Une cliente, qui a déjà bénéficié d’un prêt EL sur sa RP il y a quelques années, a souscrit un PEL et aimerait de nouveau faire un prêt EL a-t-elle le droit ? ", "Peut-on accorder un différé sur des prêt EL ?", "Le financement avec un prêt PEL pour travaux seuls ne donne-t-il pas droit à une majoration de prime (surprime PEL) ?","Dans la cadre de la succession de son père, Madame X peut-elle bénéficier du droit à prêt de son père. ?", "Si oui, quelles démarches doit-elle effectuer (n’étant pas seule héritière, je suppose  qu’elle devra nous produire  un accord du notaire chargé de la succession ou  une renonciation de son frère)?", "Dans quelles conditions peut-elle utiliser ce droit à prêt : que peut-elle financer, doit-elle utiliser en priorité le montant des capitaux du PEL cédé, le montant de la prime, etc.", "Nous sommes sollicités par des clients, locataire de leur résidence principale, détenue par une SAS dont ils détiennent l’usufruit des parts.", 
                                                   " Nous sommes sollicités pour un financement travaux résidence locative au nom de Mr et Mme sur un bien propre de Mme. Les clients sont mariés en communauté légale. Les clients souhaitent utiliser leurs droits Epargne Logement. Est-il possible d’utiliser les droits de Monsieur pour un financement sur un bien propre Mme, dans la mesure où les droits de Mr utilisés sont inférieurs à la moitié des droits totaux utilisés ?", "Les Droits à Crédits du PEL sont-ils transférables à TOUS les héritiers quel que soit leur qualité (enfant ou légataire) ?", "-Si oui, et qu’il y a plusieurs héritiers, dans quelles proportions ?", "Confirmez vous que pour recevoir les DAC, l’(les)héritier(s) doit(vent) lui(eux)-même détenir un PEL ? Depuis combien de temps au minimum ?", "Les mêmes règles de transmission par succession s’appliquent-elle pour la Droits à Crédit du CEL ?"]
        if 'selected_example_query' not in st.session_state:
            st.session_state['selected_example_query'] = ""

    def add_message_to_chat(self, message):
        st.session_state['messages'].append(message)


    def extract_feedback_details(self):
        query, answer, sources_contents = "", "", [''] * 4
        if st.session_state['messages']:
            if len(st.session_state['messages']) > 1:
                query = st.session_state['messages'][-2]["content"]
                answer = st.session_state['messages'][-1]["content"]
                sources_contents = [source_content for _, _, _, source_content in st.session_state['sources_info']] if 'sources_info' in st.session_state else sources_contents
        return query, answer, sources_contents


    def _on_feedback_submit(self, feedback_text):
        def on_feedback_submit():
            if feedback_text:
                self.submit_manual_feedback(feedback_text)
                st.session_state['manual_feedback'] = ''
        return on_feedback_submit

    def reset_conversation(self):
        st.session_state['messages'] = []
        st.session_state['sources_info'] = []
        
    def _extract_feedback_details(self):
        """Extract details for logging feedback."""
        query, answer, sources_contents = "", "", [''] * 4
        if st.session_state.get('messages'):
            if len(st.session_state['messages']) > 1:
                query = st.session_state['messages'][-2]["content"]
                answer = st.session_state['messages'][-1]["content"]
                sources_contents = [source_content for _, _, _, source_content in st.session_state.get('sources_info', [])]
        return query, answer, sources_contents

    def submit_manual_feedback(self, feedback_text):
        """Submits manual feedback."""
        if feedback_text:
            self.handle_feedback("Manual", feedback_text)