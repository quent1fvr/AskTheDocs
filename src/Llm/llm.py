from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage
from . import prompts 

class LlmAgent:
    def __init__(self, llm_model: str, client: MistralClient):
        self.llm = llm_model
        self.client = client

    def send_request_to_mistral(self, messages):
        chat_response = self.client.chat(
            model=self.llm,
            messages=messages,
            temperature=0,
            safe_prompt= True
        )
        return chat_response.choices[0].message.content

    def create_chat_message(self, role, content):
        return ChatMessage(role=role, content=content)

    def generate_paragraph(self, query: str, context, history, language='fr') -> str:
        template = prompts.GENERATE_PARAGRAPH_PROMPT.format(context=context, history=history, language=language, query=query)
        messages = [self.create_chat_message("user", template)]
        return self.send_request_to_mistral(messages)

    def generate_paragraph_v2(self, query: str, context, history, language='fr') -> str:
        template = prompts.GENERATE_PARAGRAPH_V2_PROMPT.format(query=query, context=context, history=history)
        messages = [self.create_chat_message("user", template)]
        return self.send_request_to_mistral(messages)

    def translate(self, text: str) -> str:
        template = prompts.TRANSLATE_PROMPT.format(text=text)
        messages = [self.create_chat_message("user", template)]
        return self.send_request_to_mistral(messages)
    
    def translate_v2(self, text: str) -> str:
        template = prompts.TRANSLATE_V2_PROMPT.format(text=text)
        messages = [self.create_chat_message("user", template)]
        return self.send_request_to_mistral(messages)

    def generate_answer(self, query: str, answer: str, history: str, context: str, language: str) -> str:
        template = prompts.GENERATE_ANSWER_PROMPT.format(query=query, answer=answer, history=history, context=context, language=language)
        messages = [self.create_chat_message("user", template)]
        return self.send_request_to_mistral(messages)

    def summarize_paragraph(self, prompt: str, title_doc: str = '', title_para: str = '', max_tokens: int = 700) -> str:
        template = prompts.SUMMARIZE_PARAGRAPH_PROMPT.format(prompt=prompt, title_doc=title_doc, title_para=title_para, max_tokens=max_tokens)
        messages = [self.create_chat_message("user", template)]
        return self.send_request_to_mistral(messages)

    def summarize_paragraph_v2(self, prompt: str, title_doc: str = '', title_para: str = '', location: str = '', max_tokens: int = 850) -> str:
        template = prompts.SUMMARIZE_PARAGRAPH_V2_PROMPT.format(prompt=prompt, title_doc=title_doc, title_para=title_para, location=location, max_tokens=max_tokens)
        messages = [self.create_chat_message("user", template)]
        return self.send_request_to_mistral(messages)

    def detect_language(self, text: str) -> str:
        template = prompts.DETECT_LANGUAGE_PROMPT.format(text=text)
        messages = [self.create_chat_message("user", template)]
        return self.send_request_to_mistral(messages)

    def detect_language_v2(self, text: str) -> str:
        template = prompts.DETECT_LANGUAGE_V2_PROMPT.format(text=text)
        messages = [self.create_chat_message("user", template)]
        return self.send_request_to_mistral(messages)
