GENERATE_PARAGRAPH_PROMPT = (
    "You are a conversation bot designed to answer to the query from users. "
    "Your answer is based on the context delimited by triple backticks :\n ```{context}```\n"
    "You are consistent and avoid redundancies with the rest of the initial conversation "
    "delimited by triple backticks :\n ```{history}```\n"
    "Your response shall be in {language} and shall be concise. "
    "You shall only provide the answer, nothing else before and after. "
    "Here is the query you are given :\n```{query}```"
)

GENERATE_PARAGRAPH_V2_PROMPT = ("SYSTEM :"
    "Vous êtes un robot conversationnel français conçu pour répondre aux requêtes des utilisateurs en français"
    "USER :"
    "Voici la requête à laquelle vous devez répondre : {query} en français " 
    "Si la question n'est pas liée au contexte / à l'historique suivant, vous devez répondre avec vos connaissances."    
    "Votre réponse est basée sur le contexte délimité par des triples crochets :\n ``{context}``\n"
    "L'historique de la conversation est délimité par des triples crochets :\n ``{history}``\n"
    "ASSISTANT : ")
    


TRANSLATE_PROMPT = (
    "Your task consists in translating in English the following text "
    "delimited by triple backticks: ```{text}```\n"
    "If the text is already in English, just return it!"
)

TRANSLATE_V2_PROMPT = (
    "Translate in English the text. If it is already in English, just return the text."
)

GENERATE_ANSWER_PROMPT = (
    "Your task consists in translating the answer in {language}, if it's not already the case, to the query "
    "delimited by triple backticks: ```{query}``` \n"
    "You don't add new content to the answer but: "
    "1 You can use some vocabulary from the context delimited by triple backticks:\n"
    "```{context}```\n"
    "2 You are consistent and avoid redundancies with the rest of the initial"
    "conversation delimited by triple backticks: ```{history}```\n"
    "Your response shall respect the following format:<response>\n"
    "Here is the answer you are given in {language}: {answer}"
)

SUMMARIZE_PARAGRAPH_PROMPT = (
    "Your task consists in summarizing the paragraph of the document untitled ```{title_doc}```. "
    "The paragraph title is ```{title_para}```. "
    "Your response shall be concise and shall respect the following format:<summary> "
    "If you see that the summary that you are creating will not respect ```{max_tokens}``` tokens, find a way to make it shorter. "
    "The paragraph you need to summarize is the following: {prompt}"
)

SUMMARIZE_PARAGRAPH_V2_PROMPT = (
    "Your task consists in summarizing in English the paragraph of the document untitled ```{title_doc}``` located in the ```{location}``` section of the document. "
    "The paragraph title is ```{title_para}```. "
    "Your response shall be concise and shall respect the following format:<summary> "
    "If you see that the summary that you are creating will not respect ```{max_tokens}``` tokens, find a way to make it shorter."
)

DETECT_LANGUAGE_PROMPT = (
    "Your task consists in detecting the language of the last question or sentence of the text. "
    "You should only give the two letters code of the language detected, nothing else. "
    "Here is the text you are given delimited by triple backticks: ```{text}```"
)

DETECT_LANGUAGE_V2_PROMPT = (
    "Your task consists in detecting the language of the last question or sentence of the text. "
    "You should only give the two letters code of the language detected, nothing else."
)
