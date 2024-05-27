from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.memory import ConversationBufferMemory
from langchain.prompts.chat import ChatPromptTemplate

import os
os.environ["GOOGLE_API_KEY"] = "AIzaSyBtRt__Qz9UaJmTekm9_MiqYl2AxjV-Bmw"

# Initialize LLM with desired parameters
llm = ChatGoogleGenerativeAI(
    model="gemini-pro",
    temperature=1,
    top_k=4,
    verbose=False,
    convert_system_message_to_human=True
)

# Create chat continuity memory using ConversationBufferMemory
memory = ConversationBufferMemory()

template="You are a Helpful Psychotist AI Bot.your name is Mala. give solution for user queries (always give reply within maximum of 30 words)"

human_template="{text}"
chatprompt=ChatPromptTemplate.from_messages([
    ("system",template),
    ("human",human_template)
])

chain=chatprompt|llm


def chatbot(message):
    response = chain.invoke(message)
    memory.save_context({'human':message},{'ai':response.content})
    return response.content
